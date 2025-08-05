import time
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.model.schema.autoreview import AutoReviewCreate
from app.core.auth import verify_token
from app.service.auto_review import generate_review_response, translate_ko2en
from app.utils.check import check_language

autoreview_router = APIRouter()
security = HTTPBearer()


@autoreview_router.post("/create")
def create_auto_review(
    review: AutoReviewCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security))-> dict[str, list[dict]]:
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
        username = review.username
        rating = review.rating
        storename = review.storename
        content = review.content
        iskorean = check_language(content)

        # 한글 응답 생성
        casual_text = generate_review_response(content,rating, tone="친근한", language="ko")
        formal_text = generate_review_response(content,rating, tone="정중한", language="ko")
        business_text = generate_review_response(content,rating, tone="공손한", language="ko")

        
        if iskorean:
            # 고객 리뷰가 한글로 작성된 경우 번역 생략
            casual_en_text = casual_text
            formal_en_text = formal_text
            business_en_text = business_text
        else:
            # 고객리뷰가 영어일 경우 영어 번역 요청
            casual_en_text = translate_ko2en(casual_text)
            formal_en_text = translate_ko2en(formal_text)
            business_en_text = translate_ko2en(business_text)
            
        print(f"자동 리뷰 생성 시간: {time.time() - start:.2f}초")  # 시간 측정 종료
        return {
            "results": [
                {"id": 1, "title": "친근한 버전", "text": casual_text},
                {"id": 2, "title": "정중한 버전", "text": formal_text},
                {"id": 3, "title": "공손한 버전", "text": business_text}
            ],
            "results_en": [
                {"id": 1, "title": "casual version", "text": casual_en_text},
                {"id": 2, "title": "formal version", "text": formal_en_text},
                {"id": 3, "title": "business casual version", "text": business_en_text}
            ]
        }
    except Exception as e:
        print("리뷰 응답 생성 실패:", str(e))
        raise HTTPException(status_code=500, detail="리뷰 응답 생성 중 오류 발생")
