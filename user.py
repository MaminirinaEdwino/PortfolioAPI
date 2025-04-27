
from db import Base
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean
from typing import Optional
from sqlalchemy.orm import relationship
class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    last_name = Column(String)
    first_name = Column(String)
    adress = Column(String)
    phone = Column(String)
    age = Column(Integer)
    role = Column(String, default="user") 
    is_active = Column(Boolean, default=True)
    hashed_password = Column(String)
    facebook = Column(String)
    linkedin = Column(String)
    portfolios = relationship("portfolio", back_populates="user")


# --- Data Models (Pydantic) ---
class User(BaseModel):
    id: int
    username: str
    email: str
    last_name : str
    first_name : str
    adress : str
    phone : str
    age : int
    is_active: bool = True
    facebook : str
    linkedin : str
    role: str = "user"  # Default role is 'user'
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    username: str
    password: str
    email: str
    role: str = "user"  # Default role is 'user'
    last_name : str
    first_name : str
    adress : str
    phone : str
    age : int
    facebook : str
    linkedin : str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
	
