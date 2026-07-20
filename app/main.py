from fastapi import FastAPI

from app.database.database import Base, engine
from app.database.init_db import create_admin

from app.models.user import User
from app.models.book import Book
from app.models.category import Category
from app.models.loan import Loan
from app.models.review import Review

from app.api.auth import router as auth_router
from app.api.books import router as books_router
from app.api.categories import router as categories_router
from app.api.loans import router as loans_router
from app.api.reviews import router as review_router

Base.metadata.create_all(bind=engine)

create_admin()
app = FastAPI(title="Library Management API")


app.include_router(auth_router, prefix="/api")
app.include_router(books_router, prefix="/api")
app.include_router(categories_router, prefix="/api")
app.include_router(loans_router, prefix="/api")
app.include_router(review_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Welcome to the Library Management API!"}
