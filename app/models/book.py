from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, index=True)
    author = Column(String(120), nullable=False, index=True)
    isbn = Column(String(30), nullable=False, unique=True)
    description = Column(String)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    category_id = Column(Integer, ForeignKey("categories.id"))
    created_at = Column(DateTime, default=datetime.utcnow)


    reviews = relationship("Review", back_populates="book")
    category = relationship("Category", back_populates="books")
    loans = relationship("Loan", back_populates="book")

