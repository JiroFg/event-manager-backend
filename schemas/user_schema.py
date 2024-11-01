from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated
from utils.regex_helper import email_pettern, password_pattern

class User(BaseModel):
    username: str
    email: Annotated[str, Field(min_length=1, max_lenght=30, pattern=email_pettern)]
    password: Annotated[str, Field(min_length=1, max_lenght=30, pattern=password_pattern)]

class UserLogin(BaseModel):
    email: Annotated[str, Field(min_length=1, max_lenght=30, pattern=email_pettern)]
    password: Annotated[str, Field(min_length=1, max_lenght=30, pattern=password_pattern)]

class UserDisplay(BaseModel):
    user_id: int
    username: str
    email: str
    password: str
    company_id: Optional[int] = None