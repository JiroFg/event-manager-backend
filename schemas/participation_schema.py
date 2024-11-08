from typing import Annotated, Optional
from pydantic import BaseModel, Field

class Participation(BaseModel):
    user_id: Annotated[int, Field(gt=0)]
    event_id: Annotated[int, Field(gt=0)]

class ParticipationDisplay(BaseModel):
    participation_id: int
    user_id: int
    event_id: int
    accepted: bool

class ParticipationEdit(BaseModel):
    participation_id: Annotated[int, Field(gt=0)]
    user_id: Optional[Annotated[int, Field(gt=0)]] = None
    event_id: Optional[Annotated[int, Field(gt=0)]] = None
    accepted: Optional[bool] = None