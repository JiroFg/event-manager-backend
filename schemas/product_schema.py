from typing import Annotated, Optional
from pydantic import BaseModel, Field

class Product(BaseModel):
    name: Annotated[str, Field(min_length=0, max_length=50)]
    description: Annotated[str, Field(min_length=0, max_length=400)]
    img_url: Optional[Annotated[str, Field(min_length=0, max_length=255)]] = None
    owner_id: Annotated[int, Field(gt=0)]

class ProductDisplay(BaseModel):
    product_id: int
    name: str
    description: str
    img_url: Optional[str] = None
    owner_id: int

class ProductEdit(BaseModel):
    product_id: Annotated[int, Field(gt=0)]
    name: Optional[Annotated[str, Field(min_length=0, max_length=50)]] = None
    description: Optional[Annotated[str, Field(min_length=0, max_length=400)]] = None
    img_url: Optional[Annotated[str, Field(min_length=0, max_length=255)]] = None
    owner_id: Optional[Annotated[int, Field(gt=0)]] = None