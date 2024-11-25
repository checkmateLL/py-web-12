from pydantic import BaseModel, Field
from datetime import datetime

class UserModel(BaseModel):
    email: str
    password: str = Field(min_length=6, max_length=100)


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class ContactCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    birthday: datetime | None = None
    additional_info: str | None = None

class ContactResponse(ContactCreate):
    id: int
    owner_id: int

    class Config:
        orm_mode = True