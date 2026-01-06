"""
study_service.py

유튜브 URL을 받아
→ 자막 추출
→ 문장 단위 학습 데이터로 변환
→ 프론트엔드에서 바로 사용할 수 있는 형태로 반환
"""

from app.services.youtube2 import (
    extract_video_id,
    fetch_english_transcript,
    build_youtube_play_url,
)
from app.services.sentence import split_transcript_into_sentences
from app.services.translation import translate_sentence

def create_youtube_study_data(youtube_url: str) -> dict:
    """
    유튜브 영어 학습 데이터를 생성한다.

    전체 흐름:
    1. 유튜브 URL → video_id 추출
    2. 영어 자막 조회
    3. 자막을 문장 단위로 분리
    4. 프론트엔드 친화적 데이터 구조로 가공

    Args:
        youtube_url (str): 검증된 유튜브 URL 문자열

    Returns:
        dict: 문장 단위 학습 데이터
        {
          "video_id": str,
          "sentences": [
              {
                "sentence_id": str,
                "start": float,
                "original": str,
                "translation": None,
                "play_url": str
              }
          ]
        }
    """

    # 1️⃣ video_id 추출
    video_id: str = extract_video_id(youtube_url)

    # 2️⃣ 영어 자막 가져오기
    # transcript 예시: [{ "text": "...", "start": 12.3 }, ...]
    transcript = fetch_english_transcript(video_id)

    # 3️⃣ 문장 단위로 분리
    # sentences 예시:
    # [
    #   {
    #     "sentence_id": "s_001",
    #     "start": 12.3,
    #     "original": "This is a sentence."
    #   }
    # ]
    sentences = split_transcript_into_sentences(transcript)

    # 4️⃣ 프론트엔드에서 바로 쓰기 좋은 형태로 가공
    results: list[dict] = []

    for sentence in sentences:
        start: float = float(sentence["start"])

        results.append({
            # 문장 고유 ID (프론트 key 용도)
            "sentence_id": sentence["sentence_id"],

            # 영상 시작 시간 (초 단위)
            "start": start,

            # 영어 원문
            "original": sentence["original"],

            # 번역은 Day 4에서 채울 예정
            "translation": None,

            # ▶️ 특정 시점부터 재생되는 유튜브 링크
            "play_url": build_youtube_play_url(video_id, start),
        })

    # ✅ ResponseValidationError 방지를 위해
    # 반드시 schema와 key 이름 일치
    return {
        "video_id": video_id,
        "sentences": results,
    }


translated = translate_sentence(sentence["original"])

results.append({
    "sentence_id": sentence["sentence_id"],
    "start": start,
    "original": sentence["original"],
    "translation": translated["sentence_ko"],
    "play_url": build_youtube_play_url(video_id, start),
})