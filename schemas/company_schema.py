from pydantic import BaseModel, Field
from typing import Optional
from typing_extensions import Annotated
from utils.regex_helper import url_pattern, rfc_pattern, email_pettern, zip_code_pattern

class Company(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=50)]
    commercial_name: Annotated[str, Field(min_length=1, max_length=50)]
    logo_url: Optional[Annotated[str, Field(min_length=1, max_length=255, pattern=url_pattern)]] = None
    phone: Annotated[str, Field(min_length=10, max_length=10)]
    rfc: Annotated[str, Field(pattern=rfc_pattern, max_length=50)]
    email: Annotated[str, Field(pattern=email_pettern, max_length=100)]
    website_url: Optional[Annotated[str, Field( pattern=url_pattern, max_length=255)]] = None
    employee_count: Annotated[int, Field(default=1, gt=0)]
    address: Optional[Annotated[str, Field(min_length=1, max_length=255)]] = None
    state_id: int
    zip_code: Annotated[str, Field(pattern=zip_code_pattern)]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Chedrahui",
                    "commercial_name": "Chedrahui",
                    "logo_url": None,
                    "phone": "1234567890",
                    "rfc": "VECJ880326",
                    "email": "rh@chedrahui.com.mx",
                    "website_url": None,
                    "employee_count": "1000",
                    "address": None,
                    "state_id": 15,
                    "zip_code": "01000"
                }
            ]
        }
    }

class CompanyDisplay(BaseModel):
    company_id: int
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