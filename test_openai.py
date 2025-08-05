import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# API 키 설정
openai.api_key = os.getenv("OPENAI_API_KEY")

print(f"API Key: {openai.api_key[:20]}...")

try:
    # 간단한 테스트 요청
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": "Hello, this is a test."}
        ],
        max_tokens=10
    )
    print("✅ OpenAI API 연결 성공!")
    print(f"응답: {response['choices'][0]['message']['content']}")
except Exception as e:
    print(f"❌ OpenAI API 연결 실패: {str(e)}") 