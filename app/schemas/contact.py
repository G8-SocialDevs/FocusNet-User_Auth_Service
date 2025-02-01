from pydantic import BaseModel
from typing import Optional

class ContactResponse(BaseModel):
    contactid: int
    useridprop: int
    useridrec: int
    status: int

    class Config:
        orm_mode = True

class ContactListResponse(BaseModel):
    contactid: int
    contact_user_id: int
