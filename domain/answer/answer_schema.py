from pydantic import BaseModel, field_validator


class AnswerCreate(BaseModel):
    content: str        # 답변 등록시 전달되는 파라미터 ( 필수 매개변수, 단 "" 같은 빈 문자열이 입력될 수 있다 )

    @field_validator('content')     # content 라는 파라미터에 값이 저장될 때 실행
    def not_empty(cls, v):          # cls = 클래스 자신을 나타내는 매개변수
        if not v or not v.strip():  # v = content
            raise ValueError('빈 값은 허용되지 않습니다.')  # v 가 빈 값일 경우 예외 처리 ( raise : 예외 발생 키워드 )
        return v
    