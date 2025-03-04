from pydantic import BaseModel
from typing import Optional

class ContactResponse(BaseModel):
    contactid: int
    useridprop: int
    useridrec: int
    status: int

    class Config:
        orm_mode = True

class UserProfileResponse(BaseModel):
    UserID: int
    FirstName: Optional[str]
    LastName: Optional[str]
    UserName: str
    UserImage: Optional[str]
    Bio: Optional[str]
    PhoneNumber: str

class ContactDetailResponse(BaseModel):
    contactid: int
    user: UserProfileResponse