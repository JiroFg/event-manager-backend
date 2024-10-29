from pydantic import BaseModel

class UserTypeDisplay(BaseModel):
    user_type_id: int
    name: str