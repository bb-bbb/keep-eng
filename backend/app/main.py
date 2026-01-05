"""
main.py

FastAPI 애플리케이션 진입점
"""

from fastapi import FastAPI
from app.routers import study

# FastAPI 앱 생성
app = FastAPI(
    title="YouTube English Study API",
    description="유튜브 영어 자막 기반 학습 API",
    version="0.1.0",
)

# Router 등록
app.include_router(study.router)


@app.get("/")
def health_check():
    """
    서버 상태 확인용 엔드포인트
    """
    return {"status": "ok"}
