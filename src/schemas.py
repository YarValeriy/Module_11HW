from pydantic import BaseModel, field_validator
from datetime import date, datetime
from typing import Optional


# Pydantic models for request and response data validation

class ContactBase(BaseModel):
    name: str
    surname: str
    email: str
    phone: str
    birthday: date


class ContactCreate(ContactBase):
    name: str
    surname: str = None
    email: Optional[str] = None
    phone: str
    birthday: Optional[date]
    additional_data: Optional[str] = None

    @field_validator('email')
    def check_email(cls, v):
        if v == '':
            return None
        return v


class ContactUpdate(ContactCreate):
    pass


class ContactResponse(ContactCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
