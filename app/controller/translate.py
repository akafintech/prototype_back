import time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.model.schema.translate import TranslateReviewBase
from app.core.auth import verify_token
from app.service.auto_review import translate_en2ko
from app.utils.check import check_language

trans_router = APIRouter()
security = HTTPBearer()


@trans_router.post("/review")
def translate_review(
    review: TranslateReviewBase,
    credentials: HTTPAuthorizationCredentials = Depends(security))-> dict[str, str]:
    """
    리뷰 내용 기반 자동 응답 생성 API
    """
    start = time.time()  # 시간 측정 시작
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        # 프론트에서 전달된 리뷰 정보
        target = review.target_language
        content = review.text
        iskorean = check_language(content)

        # 영어 번역 요청
        if iskorean:
            translated_text = content
        else:
            # 이미 영어로 작성된 경우 번역 생략
            translated_text = translate_en2ko(content)
        return {"translated_text": translated_text}
    except Exception as e:
        print("번역 실패:", str(e))
        raise HTTPException(status_code=500, detail="번역 중 오류 발생")
