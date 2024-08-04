# 데이터를 처리하는 코드
# 서로 다른 라우터에서 데이터를 처리하는 부분이 동일하여 중복될 수 있기 때문에 파일 분리

from models import Question
from sqlalchemy.orm import Session

'''
JPA 와 같이 DB 사용하는 방법 (터미널, fastapi 모두 사용법 동일)
1. 터미널 이용시 python3 입력 -> from database import SessionLocal, 테이블들 import -> db = SessionLocal()
2. 명령어 입력
- db.query(테이블명).명령어.기타
    - ex. db.query(Question).order_by(Question.subject.desc())
    - ex. db.query(Question).order_by(Question.subject.desc()).all()
    - ex. db.query(Question).order_by(Question.subject.desc()).count()
    - ex. db.query(Question).get(1).subject
3. 터미널 이용시 DB 저장
    - db.add(명령어 수행한 결과를 저장한 변수)
    - db.commit()   # 만약 add 한 내용을 rollback 하고 싶을 때 : db.rollback() 
'''
def get_question_list(db: Session):
    question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
        .all()
    return question_list


# 점프 투 FastAPI : 3-02 게시판 페이징
# get_question_list 개선 : 페이징 처리 (offset, limit)
# offset() : 
# limit() : 
def get_question_list(db: Session, skip: int = 0, limit: int = 10): # skip : 시작 인덱스, limit : 가져올 데이터 개수
    _question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
    
    total = _question_list.count()
    question_list = _question_list.offset(skip).limit(limit).all()
    return total, question_list     # ( 전체 건수, 페이징 적용된 질문 목록 )


# 점프 투 FastAPI : 2-10 : 질문 등록 CRUD
from datetime import datetime

from domain.question.question_schema import QuestionCreate

def create_question(db:Session, question_create: QuestionCreate):
    db_question = Question(subject=question_create.subject,
                           content=question_create.content,
                           create_date=datetime.now())
    db.add(db_question)
    db.commit()