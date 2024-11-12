from typing import Annotated
from pydantic import BaseModel, Field
from datetime import time

class Schedule(BaseModel):
    event_id: Annotated[int, Field(gt=0)]
    start_time: time
    end_time: time

class ScheduleDisplay(BaseModel):
    schedule_id: int
    event_id: int
    start_time: time
    end_time: time