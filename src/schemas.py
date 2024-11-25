from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# User Models
class UserModel(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=20)

class UserDb(BaseModel):
    id: int
    username: Optional[str]
    email: str
    created_at: datetime
    

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

# Token Models
class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# Contact Models
class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: datetime
    additional_info: Optional[str] = None

class ContactUpdate(ContactCreate):
    pass

class ContactResponse(ContactCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
