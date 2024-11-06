from typing import Optional
from pydantic import BaseModel

class TableDisplay(BaseModel):
    table_id: int
    table_num: int
    event_id: int
    user_id: Optional[int] = None