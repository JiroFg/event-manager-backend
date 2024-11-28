from typing import Annotated
from pydantic import BaseModel, Field

class Meeting(BaseModel):
    buyer_id: Annotated[int, Field(gt=0)]
    exhibitor_id: Annotated[int, Field(gt=0)]
    schedule_id: Annotated[int, Field(gt=0)]
    event_id: Annotated[int, Field(gt=0)]

class MeetingDisplay(BaseModel):
    meeting_id: int
    buyer_id: int
    exhibitor_id: int
    schedule_id: int
    event_id: int