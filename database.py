# 데이터베이스와 관련된 설정을 하는 파일
'''
데이터베이스를 사용하기 위한 변수, 함수등을 정의하고 접속할 데이터베이스의 주소와 사용자, 비밀번호등을 관리

사용할 DB : SQLAlchemy
설치 명령어 : pip install sqlalchemy
'''

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 데이터베이스 주소
# sqlite:///./원하는_이름.db : sqlite3 데이터베이스의 파일을 프로젝트의 루트 디렉토리에 저장 ( alembic.ini 파일과 경로 동일해야 함)
# SQLite : 파이썬 내장 데이터베이스
SQLALCHEMY_DATABASE_URL = "sqlite:///./myapi.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# 점프 투 FastAPI 2-04-2 의존성 주입
'''
# 데이터베이스 세션의 생성과 반환을 자동화하는 방법
import contextlib

@contextlib.contextmanager
# db 세션 객체를 리턴하는 제너레이터 get_db 함수 추가
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''        
        
# 데이터베이스 세션의 생성과 반환을 자동화하는 방법 : 추가 개선
# Depends 에서 contextmanager 를 적용하게 끔 설계되어 있기 때문에 2중 적용이 안되게기존 어노테이션을 제거해야 한다.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()