from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.database import Base

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    comment = Column(String)
    rating = Column(Integer, nullable=False)
    create_at = Column(DateTime, default=datetime.utcnow)


    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")