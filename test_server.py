import requests
import json

def test_server():
    try:
        # 기본 엔드포인트 테스트
        response = requests.get("http://localhost:8000/")
        print(f"기본 엔드포인트 응답: {response.status_code}")
        print(f"응답 내용: {response.json()}")
        
        # API 문서 확인
        response = requests.get("http://localhost:8000/docs")
        print(f"API 문서 접근: {response.status_code}")
        
        print("✅ 서버가 정상적으로 실행되고 있습니다!")
        
    except requests.exceptions.ConnectionError:
        print("❌ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    test_server() 