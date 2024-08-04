# SQLAlchemy(DB) 는 모델 기반으로 데이터베이스를 처리
# SQLAlchemy 에서 사용할 모델 정의 

# Question 모델
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base

class Question(Base):
    # __tablename__ : 모델에 의해 관리되는 테이블의 이름
    __tablename__ = "question"      

    # 변수 = Column(데이터 타입, 그외 속성)
    id = Column(Integer, primary_key=True)          # Integer : 고유 번호와 같은 숫자
                                                    # primary_key : id 속성을 기본 키(Primary Key)로 만든다
    subject = Column(String, nullable=False)        # String : 제목처럼 글자 수가 제한된 텍스트
                                                    # nullable : 값을 저장할 때 null 값을 허용할지의 여부
    content = Column(Text, nullable=False)          # Text : 글 내용처럼 글자 수를 제한할 수 없는 텍스트
    create_date = Column(DateTime, nullable=False)  # DateTime : 작성일시 같은 날짜 타입



# Answer 모델
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Answer(Base):
    __tablename__ = "answer"

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
    question_id = Column(Integer, ForeignKey("question.id"))    # 어떤 질문에 대한 답변인지 알기 위한 컬럼
                                                                # ForeignKey(외부 키) : 기존 모델과 열결된 속성 (모델을 서로 연결할 때 사용) 
    question = relationship("Question", backref="answers")      # relationship(참조할 모델명, backref : 역참조 설정)
                                                                    # 역참조 : 질문에서 답변을 거구로 참조하는 것
                                                                    
# 모델을 이용해 테이블 자동 생성 방법 : alembic
# alembic : SQLAlchemy로 작성한 모델을 기반으로 데이터베이스를 쉽게 관리할 수 있게 도와주는 도구
# ex) models.py 파일에 작성한 모델을 이용하여 테이블을 생성하고 변경 가능
'''
alembic 설치 방법 : pip install alembic

alembic 초기화 방법 : alembic init migrations
-> 프로젝트명/migrations 와 alembic.ini 파일이 생성된다.

alembic.ini 파일 수정 : sqlalchemy.url = sqlite:///./FastAPI_project.db

/migrations/env/py 파일 수정 : import models 추가, target_metadata = models.Base.metadata 로 변경

리비전 파일 생성 : alembic revision --autogenerate
-> 프로젝트 루트 디렉토리에 myapi.db 생성
-> migration/versions 디렉토리에 리비전 파일 생성 : ex) d6970b77e2a9_.py (무작위로 생성)

리비전 파일 실행하기 : alembic upgrade head

'''