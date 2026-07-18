from fastapi import FastAPI
from app.database.database import Base, engine

from app.models.user import User
from app.models.book import Book
from app.models.category import Category
from app.models.loan import Loan
from app.models.review import Review


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Library Management API")
@app.get("/")
def root():
    return {"message": "Welcome to the Library Management API!"}
