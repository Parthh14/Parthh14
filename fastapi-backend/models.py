from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = 'users'
    username = Column(String, primary_key=True)
    email = Column(String, unique=True)
    password = Column(String)
 
