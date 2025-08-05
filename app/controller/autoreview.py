import openai
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.model.schema.autoreview import AutoReviewCreate
from app.core.auth import verify_token
from app.core.config import settings

from openai import OpenAI  # ✅ openai>=1.0.0 대응

autoreview_router = APIRouter()
security = HTTPBearer()

# OpenAI 클라이언트 인스턴스화
client = OpenAI(api_key=settings.openai_api_key)


def generate_review_response(review_text: str, tone: str = "정중한", language: str = "ko") -> str:
    """
    GPT 기반 리뷰 응답 생성 함수
    """
    try:
        # 시스템 프롬프트
        system_prompt = f"""
        너는 숙박업소의 리뷰 담당 AI야. 고객의 리뷰를 기반으로 {tone} 말투로 응답을 생성해줘.
        응답은 다음 원칙을 지켜야 해:
        - 고객의 감정을 공감해줄 것
        - 문제가 있었다면 사과할 것
        - 긍정적인 표현으로 마무리
        언어는 {"한국어" if language == "ko" else "영어"}로 작성해줘.
        """.strip()

        user_prompt = f'리뷰: "{review_text}"'

        # OpenAI ChatCompletion 요청
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("OpenAI API Error:", str(e))
        raise HTTPException(status_code=500, detail="OpenAI 응답 생성 중 오류 발생")


@autoreview_router.post("/create")
def create_auto_review(
    review: AutoReviewCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    리뷰 내용 기반 자동 응답 생성 API
    """
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

        # 한글 응답 생성
        casual_text = generate_review_response(content, tone="친근한", language="ko")
        formal_text = generate_review_response(content, tone="정중한", language="ko")
        business_text = generate_review_response(content, tone="공손한", language="ko")

        # 영어 응답 생성
        casual_en_text = generate_review_response(content, tone="casual", language="en")
        formal_en_text = generate_review_response(content, tone="formal", language="en")
        business_en_text = generate_review_response(content, tone="business casual", language="en")

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
