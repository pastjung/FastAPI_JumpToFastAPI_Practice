# Pydantic : FastAPI 의 입출력 스펙을 정의하고 그 값을 검증하기 위해 사용하는 라이브러리
# Pydantic 은 FastAPI 설치시 함께 설치된다.

'''
스키마란
데이터의 구조와 명세를 의미
-> ex) 출력 스키마 : 출력 항목이 몇 개인지, 제약 조건은 어떤 것이 있는지 등을 기술하는 것을 말함

Pydantic 은 API 의 입출력 항목을 다음과 같이 정의하고 검증할 수 있다
- 입출력 항목의 갯수와 타입 설정
- 입출력 항목의 필수값 체크
- 입출력 항목의 데이터 검증

SpringBoot의 Entity 와 비슷한 개념인듯
'''

import datetime
from pydantic import BaseModel

class Question(BaseModel):
    # 모두 디폴트 값이 없기 때문에 필수항목
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    
    # 필수항목이 아닌 경우
    number: int | None = None
    
    
# 점프 투 FastAPI : 2-10 질문 등록
from pydantic import field_validator

class QuestionCreate(BaseModel):
    subject: str
    content: str
    
    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다')
        return v