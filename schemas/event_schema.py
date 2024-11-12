from typing import Annotated, Optional
from pydantic import BaseModel, Field, model_validator
from datetime import date, time, timedelta
from utils.regex_helper import url_pattern

class Event(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=60)]
    description: Annotated[str, Field(min_length=1, max_length=255)]
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    tables: Annotated[int, Field(gt=0, lt=500)]
    img_url: Optional[Annotated[str, Field(min_length=1, max_length=255, pattern=url_pattern)]] = None
    meeting_duration: Annotated[int, Field(gt=0)]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Expoanimex",
                    "description": "Expo sobre anime y videojuegos",
                    "start_date": date.today() + timedelta(days=1),
                    "end_date": date.today() + timedelta(days=2),
                    "start_time": "10:00:00",
                    "end_time": "18:00:00",
                    "tables": 1,
                    "img_url": "https://www.sopitas.com/wp-content/uploads/2023/12/historia-origen-detras-meme-artimonki-imagen-arctic-monkeys-ontario.jpeg?resize=1024,1024",
                    "meeting_duration": 30
                }
            ]
        }
    }

    @model_validator(mode="after")
    def validate_date(self):
        if self.start_date < date.today():
            raise ValueError("Start date cannot be before today")
        if self.end_date < self.start_date:
            raise ValueError("End date cannot be before start date")
        if self.end_time < self.start_time:
            raise ValueError("End time cannot be before start time")
        return self

class EventDisplay(BaseModel):
    event_id: int
    name: str
    description: str
    start_date: date
    end_date: date
    start_time: time
    end_time: time
    tables: int
    img_url: str
    meeting_duration: int

class EventEdit(BaseModel):
    event_id: Annotated[int, Field(gt=0)]
    name: Optional[Annotated[str, Field(min_length=1, max_length=60)]] = None
    description: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None 
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    tables: Optional[Annotated[int, Field(gt=0, lt=500)]] = None
    img_url: Optional[Annotated[str, Field(min_length=1, max_length=255, pattern=url_pattern)]] = None
    meeting_duration: Optional[Annotated[int, Field(gt=0)]] = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "event_id": 1,
                    "name": "Expoanimex",
                    "description": "Expo sobre anime y videojuegos",
                    "start_date": date.today() + timedelta(days=1),
                    "end_date": date.today() + timedelta(days=2),
                    "start_time": "10:00:00",
                    "end_time": "18:00:00",
                    "tables": 1,
                    "img_url": "https://www.sopitas.com/wp-content/uploads/2023/12/historia-origen-detras-meme-artimonki-imagen-arctic-monkeys-ontario.jpeg?resize=1024,1024",
                    "meeting_duration": 30
                }
            ]
        }
    }

    @model_validator(mode="after")
    def validate_date(self):
        if (self.start_date and (not self.end_date or not self.start_time or not self.end_time or not self.meeting_duration)) or (self.end_date and (not self.start_date or not self.start_time or not self.end_time or not self.meeting_duration)) or (self.start_time and (not self.start_date or not self.end_date or not self.end_time or not self.meeting_duration)) or (self.end_time and (not self.start_date or not self.end_date or not self.start_time or not self.meeting_duration)) or (self.meeting_duration and (not self.start_date or not self.end_date or not self.start_time or not self.end_time)):
            raise ValueError("Please enter start date, end date, start time, start time and meeting duration")
        if not self.start_date is None:
            if self.start_date < date.today():
                raise ValueError("Start date cannot be before today")
        if (not self.end_date is None) and (not self.start_date is None):
            if self.end_date < self.start_date:
                raise ValueError("End date cannot be before start date")
        if (not self.end_time is None) and (not self.start_time is None):
            if self.end_time < self.start_time:
                raise ValueError("End time cannot be before start time")
        return self