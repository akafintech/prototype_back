from fastapi import HTTPException
from openai import OpenAI  # ✅ openai>=1.0.0 대응
from app.core.config import settings

# OpenAI 클라이언트 인스턴스화
client = OpenAI(api_key=settings.openai_api_key)


def generate_review_response(review_text: str, rating:int, tone: str = "정중한",language: str = "ko") -> str:
    """
    GPT 기반 리뷰 응답 생성 함수
    """
    try:
        system_prompt = f"""
        너는 숙박업소의 리뷰 담당 AI야. 고객의 리뷰와 평점을 기반으로 {tone} 말투로 응답을 생성해줘.
        응답은 반드시 다음 원칙을 지켜야 해:
        1. 고객의 감정을 공감해줄 것.
        2. 문제가 있었다면 사과할 것.
        3. 긍정적인 표현으로 마무리할 것.
        4. **이모티콘을 절대로 사용하지 않을 것**.
        언어는 {"한국어" if language == "ko" else "영어"}로 작성해줘.
        """.strip()
        
        user_prompt = f'리뷰: {review_text} 평점: {rating}점'

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
    
def translate_ko2en(review_text: str) -> str:
    """
    GPT 기반 리뷰 응답 영어 번역 생성 함수
    """
    try:
        # 시스템 프롬프트
        system_prompt = f"""
        너는 숙박업소의 리뷰 번역 담당 AI야. 고객의 한글 리뷰를 영어로 번역해줘.
        """.strip()

        user_prompt = review_text

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
        raise HTTPException(status_code=500, detail="OpenAI 영어 번역 중 오류 발생")
    
def translate_en2ko(review_text: str) -> str:
    """
    GPT 기반 리뷰 응답 영어 번역 생성 함수
    """
    try:
        # 시스템 프롬프트
        system_prompt = f"""
        너는 숙박업소의 리뷰 번역 담당 AI야. 영어 리뷰를 한글로 번역해줘.
        """.strip()

        user_prompt = review_text

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
        raise HTTPException(status_code=500, detail="OpenAI 영어 번역 중 오류 발생")