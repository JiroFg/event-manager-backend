from typing import Annotated, Optional
from pydantic import BaseModel, Field

class ExtraTables(BaseModel):
    tables: Annotated[int, Field(gt=0)]
    event_id: Annotated[int, Field(gt=0)]

class TableDisplay(BaseModel):
    table_id: int
    table_num: int
    event_id: int
    user_id: Optional[int] = None

class TableUpdate(BaseModel):
    table_id: Annotated[int, Field(gt=0)]
    user_id: Annotated[int, Field(gt=0)]