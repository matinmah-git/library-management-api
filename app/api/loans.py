from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone
from app.models.book import Book
from app.models.loan import Loan
from app.schemas.loan import LoanResponse, LoanCreate
from app.core.security import current_user, require_roles
from app.database.database import get_db
from app.models.user import User
from app.schemas.user import MessageResponse

router = APIRouter(prefix="/loans", tags=["loans"])


@router.get("/", response_model=list[LoanResponse])
def get_all_loans(db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin","librarian"))):
    return db.query(Loan).all()

@router.get("/me", response_model=LoanResponse)
def get_my_loans(db: Session = Depends(get_db), current_user: User = Depends(current_user)):
    return db.query(Loan).filter(Loan.user_id == current_user.id).all()

@router.post("/", response_model=LoanResponse)
def borrow_book(loan_data: LoanCreate, db: Session = Depends(get_db), current_user: User = Depends(current_user)):

    book = db.query(Book).filter(Book.id == loan_data.book_id).first()
    existing_book = db.query(Loan).filter(Loan.user_id == current_user.id, Loan.book_id == loan_data.book_id, Loan.returned == False ).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    if book.available_copies <= 0 :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No copies available")
    if existing_book:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already borrowed this book")

    new_loan = Loan(user_id=current_user.id, book_id=loan_data.book_id, due_date=loan_data.due_date)

    book.available_copies -= 1

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    return new_loan

@router.put("/return/{loan_id}", response_model=MessageResponse)
def return_book(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):

    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    book = db.query(Book).filter(Book.id == loan.book_id).first()

    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")
    if current_user.role == "member" and current_user.id != loan.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")
    if loan.returned :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already returned")

    loan.returned = True
    loan.return_date = datetime.now(timezone.utc)
    book.available_copies += 1

    db.commit()

    return MessageResponse(message="Book returned successfully")

@router.delete("/{loan_id}", response_model=MessageResponse)
def delete_loan(loan_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_roles("admin","librarian"))):

    loan = db.query(Loan).filter(Loan.id == loan_id).first()

    if not loan:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Loan not found")

    db.delete(loan)
    db.commit()

    return MessageResponse(message="Loan deleted successfully")