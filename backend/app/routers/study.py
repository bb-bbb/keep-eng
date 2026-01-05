# HTTP 요청 처리
# 예외 → HTTP status 변환
# 절대 로직 직접 처리 안 함


from fastapi import APIRouter, HTTPException, status

from app.schemas.study import (
    YouTubeStudyRequest,
    YouTubeStudyResponse,
)
from app.services.study_service import create_youtube_study_data

router = APIRouter(
    prefix="/api/study",
    tags=["Study"],
)


@router.post(
    "/youtube",
    response_model=YouTubeStudyResponse,
    status_code=status.HTTP_200_OK,
)
def study_youtube(request: YouTubeStudyRequest):
    """
    유튜브 영어 학습용 자막 데이터를 생성하는 API

    Flow:
    1. URL 검증 (Pydantic)
    2. 자막 추출 서비스 호출
    3. 결과 반환
    """

    try:
        return create_youtube_study_data(str(request.youtube_url))

    except ValueError as e:
        # URL 형식 오류, video_id 추출 실패 등
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except RuntimeError as e:
        # 자막 없음 / 자막 비활성화
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )

    except Exception as e:
        print("🔥 UNEXPECTED ERROR:", repr(e))
        raise HTTPException(
            status_code=500,
            detail=str(e),  # ← 임시로 메시지 노출
        )