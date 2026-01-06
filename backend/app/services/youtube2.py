"""
youtube2.py

유튜브 자막 관련 모든 로직을 담당하는 서비스 모듈
- URL에서 video_id 추출
- YouTube Transcript API 연동
- 영어 자막을 데이터 형태로 반환
"""

from urllib.parse import urlparse, parse_qs
from typing import List, Dict
from youtube_transcript_api import YouTubeTranscriptApi
import logging

# 로거 설정
logger = logging.getLogger(__name__)


class TranscriptError(Exception):
    """자막 관련 커스텀 예외"""
    pass


class TranscriptNotFoundError(TranscriptError):
    """자막을 찾을 수 없을 때"""
    pass


class TranscriptDisabledError(TranscriptError):
    """자막이 비활성화되었을 때"""
    pass


def extract_video_id(youtube_url: str) -> str:
    """
    다양한 유튜브 URL 형태에서 video_id를 추출한다.
    
    지원 형식:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/live/VIDEO_ID
    
    Args:
        youtube_url: 유튜브 URL 문자열
        
    Returns:
        str: 추출된 video_id
        
    Raises:
        ValueError: URL 형식이 지원되지 않을 때
        
    Examples:
        >>> extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
        >>> extract_video_id("https://youtu.be/dQw4w9WgXcQ")
        'dQw4w9WgXcQ'
    """
    if not youtube_url or not isinstance(youtube_url, str):
        raise ValueError("Invalid YouTube URL: URL must be a non-empty string")
    
    parsed_url = urlparse(youtube_url)
    video_id = None

    # youtu.be/VIDEO_ID
    if parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path.lstrip("/").split("?")[0]

    # youtube.com 계열
    elif parsed_url.hostname and "youtube.com" in parsed_url.hostname:
        # https://www.youtube.com/watch?v=VIDEO_ID
        if parsed_url.path == "/watch":
            video_id = parse_qs(parsed_url.query).get("v", [None])[0]

        # https://www.youtube.com/shorts/VIDEO_ID
        elif parsed_url.path.startswith("/shorts/"):
            parts = parsed_url.path.split("/")
            video_id = parts[2] if len(parts) > 2 else None

        # https://www.youtube.com/live/VIDEO_ID
        elif parsed_url.path.startswith("/live/"):
            parts = parsed_url.path.split("/")
            video_id = parts[2] if len(parts) > 2 else None

    if not video_id or len(video_id) != 11:  # YouTube video_id는 항상 11자
        raise ValueError(
            f"Unsupported YouTube URL format or invalid video_id: {youtube_url}"
        )

    return video_id


def fetch_english_transcript(video_id: str) -> List[Dict[str, any]]:
    """
    영어 자막을 가져오는 함수
    
    수동 생성된 자막을 우선 시도하고, 없으면 자동 생성 자막 사용
    
    Args:
        video_id: 유튜브 비디오 ID (11자 문자열)
        
    Returns:
        List[Dict]: 자막 데이터 리스트
            [
                {"text": "Hello", "start": 0.0},
                {"text": "World", "start": 2.5},
                ...
            ]
        
    Raises:
        TranscriptDisabledError: 자막이 비활성화됨
        TranscriptNotFoundError: 영어 자막이 없음
        TranscriptError: 기타 자막 관련 오류
        
    Examples:
        >>> transcript = fetch_english_transcript("dQw4w9WgXcQ")
        >>> transcript[0]
        {'text': "[♪♪♪]", 'start': 1.36}
    """
    if not video_id or len(video_id) != 11:
        raise ValueError(f"Invalid video_id: {video_id}")
    
    try:
        api = YouTubeTranscriptApi()
        
        # 1. 사용 가능한 자막 목록 확인
        try:
            transcript_list = api.list(video_id)
            available_transcripts = str(transcript_list)
            
            logger.info(f"Available transcripts for {video_id}: {available_transcripts[:200]}")
            
        except Exception as list_error:
            error_msg = str(list_error).lower()
            
            if 'disabled' in error_msg:
                raise TranscriptDisabledError(
                    f"Transcripts are disabled for video: {video_id}"
                )
            elif 'private' in error_msg or 'unavailable' in error_msg:
                raise TranscriptNotFoundError(
                    f"Video is private or unavailable: {video_id}"
                )
            else:
                raise TranscriptError(
                    f"Failed to list transcripts: {str(list_error)}"
                )
        
        # 2. 영어 자막 존재 여부 확인
        if 'en' not in available_transcripts.lower():
            raise TranscriptNotFoundError(
                f"No English transcript found for video: {video_id}"
            )
        
        # 3. 자막 가져오기
        try:
            raw_transcript = api.fetch(video_id, ['en'])
        except Exception as fetch_error:
            raise TranscriptError(
                f"Failed to fetch transcript: {str(fetch_error)}"
            )
        
        # 4. 데이터 변환 및 검증
        if not raw_transcript:
            raise TranscriptNotFoundError(
                f"Transcript is empty for video: {video_id}"
            )
        
        transcript_data = []
        for item in raw_transcript:
            try:
                transcript_data.append({
                    "text": item.text.strip(),
                    "start": float(item.start),
                })
            except (AttributeError, ValueError) as e:
                logger.warning(f"Skipping invalid transcript item: {e}")
                continue
        
        if not transcript_data:
            raise TranscriptError("No valid transcript items found")
        
        logger.info(f"Successfully fetched {len(transcript_data)} transcript items")
        return transcript_data
        
    except (TranscriptDisabledError, TranscriptNotFoundError, TranscriptError):
        # 커스텀 예외는 그대로 전파
        raise
        
    except Exception as e:
        # 예상치 못한 오류
        logger.error(f"Unexpected error fetching transcript for {video_id}: {e}", exc_info=True)
        raise TranscriptError(f"Unexpected error: {str(e)}")
    
    
def build_youtube_play_url(video_id: str, start: float) -> str:
    """
    유튜브 영상 재생 URL 생성

    예:
    https://www.youtube.com/watch?v=VIDEO_ID&t=123s
    """

    start_seconds = int(start)
    return f"https://www.youtube.com/watch?v={video_id}&t={start_seconds}s"