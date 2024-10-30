from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    name: str
    commercial_name: str
    logo_url: Optional[str] = None
    phone: str
    rfc: str
    email: str
    website_url: Optional[str] = None
    employee_count: int
    address: Optional[str] = None
    state_id: int
    zip_code: str