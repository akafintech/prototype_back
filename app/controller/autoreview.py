import random
from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.model.schema.autoreview import AutoReviewCreate
from app.core.auth import verify_token  

autoreview_router = APIRouter()
security = HTTPBearer()

@autoreview_router.post("/create")
def get_reviews(review:AutoReviewCreate,
                credentials: HTTPAuthorizationCredentials = Depends(security)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 프론트에서 받은 정보
    username = review.username # 답변한 고객의 이름
    rating = review.rating # 고객이 남긴 평점
    storename = review.storename # 고객이 리뷰를 남긴 가게 이름
    content = review.content # 고객이 남긴 리뷰 내용

    # 여기서 content를 기반으로 자동 생성된 답변을 생성하는 로직을 추가.
    # 시스템 프롬프트 등...



    # 한글 생성한 답변
    casual_text = "한글 간단한 버전 생성하면 여기에 넣기"
    formal_text = "한글 정중한 버전 생성하면 여기에 넣기"
    business_text = "한글 공손한 버전 생성하면 여기에 넣기"

    # 영어 생성한 답변
    casual_en_text = "영어 간단한 버전 생성하면 여기에 넣기"
    formal_en_text = "영어 정중한 버전 생성하면 여기에 넣기"
    business_en_text = "영어 공손한 버전 생성하면 여기에 넣기"

    return {
        "results": [
            {"id":1,"title": "간결한 버전", "text": casual_text},
            {"id":2,"title": "정중한 버전", "text": formal_text},
            {"id":3,"title": "공손한 버전", "text": business_text}
        ],
        "results_en":[
            {"id":1,"title": "casual version", "text": casual_en_text},
            {"id":2,"title": "formal version", "text": formal_en_text},
            {"id":3,"title": "business casual version", "text": business_en_text}
        ]
    }