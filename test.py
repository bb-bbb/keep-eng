# test_youtube.py 파일 생성
from youtube_transcript_api import YouTubeTranscriptApi

# 테스트할 유튜브 비디오 ID (짧은 영어 영상)
video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up

try:
    # 방법 1: 클래스 메서드로 시도
    print("방법 1 시도...")
    result = YouTubeTranscriptApi.get_transcript(video_id)
    print("성공! get_transcript 사용")
    print(result[:2])
except AttributeError as e:
    print(f"방법 1 실패: {e}")
    
    try:
        # 방법 2: 인스턴스 생성
        print("\n방법 2 시도...")
        api = YouTubeTranscriptApi()
        
        # list 메서드로 사용 가능한 자막 확인
        transcripts = api.list(video_id)
        print(f"사용 가능한 자막: {transcripts}")
        
        # fetch로 자막 가져오기
        result = api.fetch(video_id, ['en'])
        print("성공! list + fetch 사용")
        print(result[:2])
    except Exception as e2:
        print(f"방법 2 실패: {e2}")