from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, PastDate, ConfigDict
#import pydantic


from src.schemas.user import UserResponse



class ContactSchema(BaseModel):
    first_name: str = Field(min_length=2, max_length=20)
    last_name: str = Field(min_length=2, max_length=20)
    #email: EmailStr
    email: str
    phone_number: str = Field(min_length=8, max_length=13)
    birthday: PastDate
    additional_info: str = Field(max_length=200)





class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    #email: EmailStr
    email: str
    phone_number: str
    birthday: PastDate
    additional_info: str
    created_at: datetime | None
    updated_at: datetime | None
    user: UserResponse | None
    model_config = ConfigDict(from_attributes = True)  # noqa
