from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "User"

    UserID = Column(Integer, primary_key=True, index=True, autoincrement=True)
    Email = Column(String(50), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    FirstName = Column(String(25))
    LastName = Column(String(25))
    UserName = Column(String(25))
    UserImage = Column(String(500))
    Bio = Column(String(1000))
    PhoneNumber = Column(String(9))