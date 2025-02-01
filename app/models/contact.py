from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.database import Base

class Contact(Base):
    __tablename__ = 'Contact'

    ContactID = Column(Integer, primary_key=True, index=True)
    UserIDProp = Column(Integer, ForeignKey('User.UserID'))
    UserIDRec = Column(Integer, ForeignKey('User.UserID'))
    Status = Column(Integer)

    # Relaciones
    user_property = relationship("User", foreign_keys=[UserIDProp])
    user_receiver = relationship("User", foreign_keys=[UserIDRec])