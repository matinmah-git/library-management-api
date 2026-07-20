from sqlalchemy import Column, Integer, String, DateTime , Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    hashed_password = Column(String(120), nullable=False)
    role = Column(String(50), nullable=False, default='member')
    is_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)


    loans = relationship("Loan", back_populates="user")
    reviews = relationship("Review", back_populates="user")
