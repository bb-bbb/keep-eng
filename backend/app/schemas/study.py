"""
study.py (schemas)

FastAPI request / response 모델 정의
"""

from typing import List
from pydantic import BaseModel, HttpUrl


class YouTubeStudyRequest(BaseModel):
    """
    유튜브 학습 요청 스키마
    """
    youtube_url: HttpUrl


class TranscriptItem(BaseModel):
    """
    자막 한 줄 데이터 구조
    """
    text: str
    start: float


class YouTubeStudyResponse(BaseModel):
    """
    유튜브 학습 응답 스키마
    """
    video_id: str
    transcript: List[TranscriptItem]
