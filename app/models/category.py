from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database.database import Base

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name =  Column(String, nullable=False, unique=True, index=True)

    books = relationship("Book", back_populates="category")