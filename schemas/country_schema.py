from pydantic import BaseModel

class CountryDisplay(BaseModel):
    name: str
    iso: str