from pydantic import BaseModel, validator
import datetime

class UserCreate(BaseModel):
    username: str
    password: str
    password_confirm: str

    @validator('username', 'password', 'password_confirm')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Empty values are not allowed")
        return v

    @validator('password_confirm')
    def pw_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError("Passwords don't match")
        return v

class Token(BaseModel):
    access_token: str
    token_type: str
    username: str
    user_idx: int

class User(BaseModel):
    id: int
    username: str
    participated: int = None
    ranking: int = None
    register_date: datetime.datetime | None = None

    class Config:
        orm_mode = True