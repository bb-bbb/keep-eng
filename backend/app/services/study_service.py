"""
study_service.py

학습 관련 비즈니스 로직을 담당
현재 단계:
- 유튜브 URL → 자막 데이터 생성

향후 확장:
- 문단 분리
- 숙어 추출
- 반복 학습 스케줄링
"""

from typing import Dict, List
from app.services.youtube2 import extract_video_id, fetch_english_transcript


def create_youtube_study_data(youtube_url: str) -> Dict:
    """
    유튜브 영어 학습용 데이터를 생성하는 함수

    Args:
        youtube_url (str): 유튜브 영상 URL

    Returns:
        Dict:
        {
            "video_id": "...",
            "transcript": [{text, start}, ...]
        }
    """
    youtube_url = str(youtube_url)

    # 1️⃣ URL에서 video_id 추출
    video_id = extract_video_id(youtube_url)

    # 2️⃣ 영어 자막 데이터 가져오기
    transcript = fetch_english_transcript(video_id)

    # 3️⃣ 결과 반환
    # (Day 3 이후 이 구조는 확장될 예정)
    return {
        "video_id": video_id,
        "transcript": transcript,
    }
