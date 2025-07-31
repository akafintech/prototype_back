import random
from fastapi import APIRouter,Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.recommend import recommend_data
from app.model.schema.recommend import RecommendCreate
from app.core.auth import verify_token  

recommend_router = APIRouter()
security = HTTPBearer()

@recommend_router.post("/create")
def get_reviews(recommend:RecommendCreate,
                credentials: HTTPAuthorizationCredentials = Depends(security)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username = recommend.username
    rating = recommend.rating
    storename = recommend.storename

    long_short = "short" if rating > 4 else "long"
    index = random.randint(0,4)

    # 한글
    casual_text = recommend_data["casual"][long_short][index]
    formal_text = recommend_data["formal"][long_short][index]
    business_text = recommend_data["business"][long_short][index]

    casual_text = casual_text.replace("00님", f"{username}님")
    formal_text = formal_text.replace("00님", f"{username}님")
    business_text = business_text.replace("00님", f"{username}님")

    casual_text = casual_text.replace("00호텔", storename)
    formal_text = formal_text.replace("00호텔", storename)
    business_text = business_text.replace("00호텔", storename)

    #영어
    casual_en_text = recommend_data["casual_en"][long_short][index]
    formal_en_text = recommend_data["formal_en"][long_short][index]
    business_en_text = recommend_data["business_en"][long_short][index]

    casual_en_text = casual_en_text.replace("00,", f"{username},")
    formal_en_text = formal_en_text.replace("00,", f"{username},")
    business_en_text = business_en_text.replace("00,", f"{username},")

    casual_en_text = casual_en_text.replace("00,", f"{username},")
    formal_en_text = formal_en_text.replace("00,", f"{username},")
    business_en_text = business_en_text.replace("00,", f"{username},")

    return {
        "results": [
            {"id":1,"title": "간결한 버전", "text": casual_text},
            {"id":2,"title": "공손한 버전", "text": formal_text},
            {"id":3,"title": "친근한 버전", "text": business_text}
        ],
        "results_en":[
            {"id":1,"title": "casual version", "text": casual_en_text},
            {"id":2,"title": "formal version", "text": formal_en_text},
            {"id":3,"title": "business casual version", "text": business_en_text}
        ]
    }