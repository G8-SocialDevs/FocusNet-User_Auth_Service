from fastapi import FastAPI
from app.api import user
from app.api import profiles
from app.api import contact

app = FastAPI()

app.include_router(user.router, prefix="/users", tags=["users"])
app.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
app.include_router(contact.router, prefix="/contacts", tags=["contacts"])