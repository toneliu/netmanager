from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
    user: 'UserResponse'


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str
    role: Optional[str] = "viewer"


class UserResponse(UserBase):
    id: int
    role: str

    model_config = {
        "from_attributes": True
    }


Token.model_rebuild()
