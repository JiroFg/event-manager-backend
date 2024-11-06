from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated
from utils.regex_helper import email_pettern, password_pattern

class User(BaseModel):
    username: str
    email: Annotated[str, Field(min_length=1, max_lenght=30, pattern=email_pettern)]
    password: Annotated[str, Field(min_length=1, max_lenght=30, pattern=password_pattern)]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "tilin",
                    "email": "tilin@gmail.com",
                    "password": "Tilin125",
                }
            ]
        }
    }

class UserLogin(BaseModel):
    email: Annotated[str, Field(min_length=1, max_lenght=30, pattern=email_pettern)]
    password: Annotated[str, Field(min_length=1, max_lenght=30, pattern=password_pattern)]

class UserDisplay(BaseModel):
    user_id: int
    username: str
    email: str
    user_type_id: int
    company_id: Optional[int] = None
    is_active: bool

class UserEdit(BaseModel):
    user_id: int
    company_id: Optional[int] = None
    is_active: Optional[bool] = None