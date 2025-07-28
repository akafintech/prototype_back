# Lemong Backend

FastAPI, PostgreSQL, SQLAlchemy를 사용한 백엔드 API 서버입니다.

## 설치 및 설정

### 1. 가상환경 활성화
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

### 3. PostgreSQL 데이터베이스 설정
1. PostgreSQL을 설치하고 데이터베이스를 생성합니다.
2. `config.py` 파일에서 데이터베이스 연결 정보를 수정합니다:
   ```python
   database_url: str = "postgresql://username:password@localhost:5432/lemong_db"
   ```

### 4. 환경 변수 설정 (선택사항)
`.env` 파일을 생성하고 다음 내용을 추가합니다:
```
DATABASE_URL=postgresql://username:password@localhost:5432/lemong_db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 서버 실행

```bash
python run_server.py
```

또는

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버가 실행되면 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 엔드포인트

### 인증 관련
- `POST /register` - 회원가입
- `POST /login` - 로그인
- `GET /me` - 현재 사용자 정보 조회

### 요청 예시

#### 회원가입
```bash
curl -X POST "http://localhost:8000/register" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "username": "testuser",
       "password": "password123"
     }'
```

#### 로그인
```bash
curl -X POST "http://localhost:8000/login" \
     -H "Content-Type: application/json" \
     -d '{
       "email": "user@example.com",
       "password": "password123"
     }'
```

#### 사용자 정보 조회
```bash
curl -X GET "http://localhost:8000/me" \
     -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 프론트엔드 연동

프론트엔드는 `C:\workspace\le_mong\lemong_front\src\pages\apply` 경로에 있으며, 
로그인/회원가입 기능이 구현되어 있습니다.

## 보안

- 비밀번호는 bcrypt로 해싱됩니다
- JWT 토큰을 사용한 인증
- CORS 설정으로 프론트엔드와 연동 
