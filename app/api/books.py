
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import require_roles
from app.models.book import Book
from app.models.user import User
from app.schemas.book import BookCreate, BookUpdate, BookResponse
from app.database.database import get_db
router = APIRouter(prefix="/books", tags=["books"])

@router.get("/", response_model=list[BookResponse])
def get_books(db:Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@router.get("/{book_id}", response_model=BookResponse):
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

@router.delete("/{book_id}")
def delete_book(book_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin"))):

    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}