from pydantic import BaseModel

class StateDisplay(BaseModel):
    state_id: int
    name: str
    abbr: str
    country_iso: str