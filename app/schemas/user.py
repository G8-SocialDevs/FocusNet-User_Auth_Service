from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    Email: EmailStr
    Password: str
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    UserName: str
    UserImage: Optional[str] = None
    Bio: Optional[str] = None
    PhoneNumber: str

class UserCreationResponse(BaseModel):
    UserID: int
    message: str

class LoginResponse(BaseModel):
    Status: str
    UserID: int
    FirstName: Optional[str]
    LastName: Optional[str]
    UserName: str
    UserImage: Optional[str]
    Bio: Optional[str]
    PhoneNumber: str