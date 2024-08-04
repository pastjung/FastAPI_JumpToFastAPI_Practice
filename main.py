# FastAPI 프로젝트의 전체적인 환경을 설정하는 파일

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5173", # Svelte (Frontend) 서버
]

# FastAPI 애플리케이션에 CORS 미들웨어 추가 : 다른 도메인에서 리소스 접근 허용
app.add_middleware(
    CORSMiddleware,
    
    # 리스트 origins 의 도메인에서 오는 요청 허용
    allow_origins=origins,
    
    # 클라이언트 요청에 쿠키와 인증 정보를 포함할 수 있도록 허용 ( False 일 경우 CORS 정책에 의해 인증 정보가 포함된 요청이 차단될 수 있다 )
    allow_credentials=True,     
    
    # 허용할 HTTP 메서드 지정 : 여기서는 모든 메서드 허용 ( ex. "GET", "POST" )
    allow_methods=["*"],
    
    # 허용할 HTTP 헤더 지정 : 여기서는 모든 헤더 허용
    allow_headers=["*"],
)

# 서버 확인용 예시 코드
@app.get("/hello")
def hello():
    return {"message": "안녕하세요 파이보"}


# question_router.py 파일의 router 객체 등록
from domain.question import question_router
app.include_router(question_router.router)


# answer_router.py 파일의 router 객체 등록
from domain.answer import answer_router
app.include_router(answer_router.router)