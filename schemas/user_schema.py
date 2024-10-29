from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserDisplay(BaseModel):
    user_id: int
    username: str
    email: str
    password: str
    company_id: Optional[int] = None