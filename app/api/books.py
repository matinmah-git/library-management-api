from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional
from app.core.security import require_roles
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.schemas.user import MessageResponse
from app.database.database import get_db
router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[BookResponse])
def get_books(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    available: Optional[bool] = None,
    author: Optional[str] = None,
    title: Optional[str] = None,
    sort: Optional[str] = None,
    db: Session = Depends(get_db),
):

    query = db.query(Book)

    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.author.ilike(f"%{search}%"),
                Book.isbn.ilike(f"%{search}%"),
            )
        )

    if category_id:
        query = query.filter(Book.category_id == category_id)
    if available:
        query = query.filter(Book.available_copies > 0)
    if available is False:
        query = query.filter(Book.available_copies == 0)
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    if title:
        query = query.filter(Book.title.ilike(f"%{title}"))

    if sort == "title":
        query = query.order_by(Book.title)

    elif sort == "-title":
        query = query.order_by(Book.title.desc())

    elif sort == "author":
        query = query.order_by(Book.author)

    elif sort == "-author":
        query = query.order_by(Book.author.desc())

    elif sort == "created_at":
        query = query.order_by(Book.created_at)

    elif sort == "-created_at":
        query = query.order_by(Book.created_at.desc())


    books = query.offset((page - 1) * size).limit(size).all()

    return books


@router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, db:Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/", response_model=BookResponse)
def create_book(book_data: BookCreate, db:Session = Depends(get_db), current_user: User = Depends(require_roles("admin", "librarian"))):
    existing_book = db.query(Book).filter(Book.isbn == book_data.isbn).first()
    if existing_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Book already exists")

    new_book = Book(**book_data.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book_data: BookUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin", "librarian"))):

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    update_data = book_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book

@router.delete("/{book_id}", response_model=MessageResponse)
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin"))):

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()

    return MessageResponse(message = "Book deleted successfully")