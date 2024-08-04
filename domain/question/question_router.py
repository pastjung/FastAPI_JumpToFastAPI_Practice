'''
라우팅이란
FastAPI 가 요청받은 URL을 해석하여 그에 맞는 함수를 실행하여 그 결과를 리턴하는 행위
'''

from fastapi import APIRouter

from database import SessionLocal, get_db
from models import Question

# APIRouter 클래스로 생성한 객체 / 점프 투 FastAPI 2-04-1 라우터
router = APIRouter(
    # prefix 속성 : 요청 URL에 항상 포함되어야 하는 값 ( SpringBoot 의 @RequestMapping() 과 같은 기능 )
    prefix="/api/question",
)

# 점프 투 FastAPI 2-04-2 의존성 주입
# APIRouter 클래스로 생성한 객체 router 를 FastAPI 앱에 등록
'''
@router.get("/list")
def question_list():
    db = SessionLocal()     # DB 세션 생성
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all() # 질문 목록 조회
    db.close()              # 사용한 세션을 커넥션 풀에 반납 ( 세션 종료 X )
    return _question_list   # 조회한 질문 목록 반환
'''


# qustion_list() 개선 : 데이터베이스 세션 자동화
# 오류 여부에 상관없이 with 문을 벗어나는 순간 db.close() 가 실행되므로 보다 안전한 코드로 개선
'''
from database import get_db

@router.get("list")
def question_list():
    with get_db() as db:
        _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list
'''

# question_list() 추가 개선 : Depends 를 사용하여 with 문보다 더 간단하게 사용하기
# get_db 함수를 with 문과 함께 쓰는 대신 question_list 함수의 매개변수로 db: Session = Depends(get_db) 객체 주입
# db: Session = Depends(get_db) : db 객체가 Session 타입임을 의미
# FastAPI 의 Depends : 매개변수로 전달 받은 함수를 실행시킨 결과를 리턴 -> db 객체에는 get_db 제너레이터에 의해 생성된 세션 객체가 주입된다.
from fastapi import Depends
from sqlalchemy.orm import Session
'''
@router.get("/list")
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question).order_by(Question.create_date.desc()).all()
    return _question_list
'''

# 점프 투 FastAPI 2-04-3 스키마
# question_list() 추가 개선 : 라우터에 Pydantic 적용하기
from domain.question import question_schema
'''
# @router.get 어노테이션에 response_model 속성 추가 : question_list 함수의 리턴값은 Question 스키마로 구성된 리스트라고 명시
@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
        .all()
    return _question_list
'''

# 점프 투 FastAPI 2-04-4 CRUD
# question_crud.py 와 question_router.py 로 파일 분리
from domain.question import question_crud

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)
    return _question_list


# 점프 투 FastAPI 2-10 질문 등록
from starlette import status

@router.post("/create", status_code=status.HTTP_204_NO_CONTENT) # 리턴할 응답이 없을 경우 응답코드 204를 리턴 : "응답 없음"
def question_create(_question_create: question_schema.QuestionCreate,
                    db:Session = Depends(get_db)):
    question_crud.create_question(db=db, question_create=_question_create)
