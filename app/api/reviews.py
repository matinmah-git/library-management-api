from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import current_user
from app.database.database import get_db
from app.models.book import Book
from app.models.review import Review
from app.models.user import User
from app.schemas.review import ReviewResponse, ReviewCreate, ReviewUpdate
from app.schemas.user import MessageResponse
router =APIRouter(prefix="/reviews", tags=["reviews"])


@router.get("/", response_model=list[ReviewResponse])
def get_reviews(db: Session = Depends(get_db)):
    return db.query(Review).all()

@router.get("/{book_id}", response_model=ReviewResponse)
def get_book_review(book_id: int, db: Session = Depends(get_db)):
    return db.query(Review).filter(Review.book_id == book_id).first()

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED_OK)
def create_review(review_data: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(current_user)):

    if db.query(Book).filter(Book.id == review_data.book_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND_CONFLICT, detail="Book not found")
    if db.query(Review).filter(Review.user_id == current_user.id, Review.book_id == review_data.book_id).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You have already reviewed this book")

    review = Review(user_id=current_user.id, **review_data.model_dump())

    db.add(review)
    db.commit()
    db.refresh(review)

    return review

@router.put("/{review_id}", response_model=ReviewResponse)
def update_review(review_data: ReviewUpdate, review_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):

    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found")
    if current_user.role == "member" and current_user.id != review.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permission denied")

    update_review = review_data.model_dump(exclude_unset=True)

    for key, value in update_review.items():
        setattr(review, key, value)

    db.commit()
    db.refresh(review)

    return review

@router.delete("/{review_id}",response_model=MessageResponse,)
def delete_review( review_id: int, db: Session = Depends(get_db), current_user: User = Depends(current_user)):

    review = db.query(Review).filter(Review.id == review_id).first()

    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Review not found.")
    if  current_user.role == "member" and review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Permission denied.")

    db.delete(review)
    db.commit()

    return MessageResponse(message="Review deleted successfully.")

