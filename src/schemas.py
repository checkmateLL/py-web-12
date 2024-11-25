from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class UserCreate(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True

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
    owner_id: int

    class Config:
        orm_mode = True