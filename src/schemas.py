from pydantic import BaseModel
from typing import Optional
from datetime import date

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: date
    additional_info: Optional[str] = None

class ContactUpdate(ContactCreate):
    pass

class ContactResponse(ContactCreate):
    id: int

    class Config:
        orm_mode = True