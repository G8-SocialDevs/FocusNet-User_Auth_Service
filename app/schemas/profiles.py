from pydantic import BaseModel
from typing import Optional

class ProfileResponse(BaseModel):
    UserID: int
    FirstName: Optional[str]
    LastName: Optional[str]
    UserName: str
    UserImage: Optional[str]
    Bio: Optional[str]
    PhoneNumber: str

class ProfileUpdate(BaseModel):
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    UserName: Optional[str] = None
    UserImage: Optional[str] = None
    Bio: Optional[str] = None
    PhoneNumber: Optional[str] = None