import datetime
from pydantic import BaseModel, validator
from domain.user.user_schema import User

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None
    voters: list[User] = []
    is_markdown: bool = False

    class Config:
        orm_mode = True

class AnswerCreate(BaseModel):
    content: str
    is_markdown: bool

    @validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Empty values are not allowed')
        return v

class AnswerUpdate(AnswerCreate):
    answer_id: int
    is_markdown: bool

class AnswerDelete(BaseModel):
    answer_id: int

class AnswerVote(BaseModel):
    answer_id: int