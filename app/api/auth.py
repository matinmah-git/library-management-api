from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database.database import get_db
import app.schemas.user
from app.schemas.user import UserCreate, UserResponse, MessageResponse, UserLogin, Token
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token, current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=MessageResponse , status_code=status.HTTP_201_CREATED)
def register(user_data = UserCreate , db:Session = Depends(get_db)):

    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email already exists")

    new_user = User(username=user_data.username, email=user_data.email, hashed_password=hash_password(user_data.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return MessageResponse(message="User registered successfully")


@router.post("/login", response_model=Token )
def login(user_data: UserLogin, db:Session = Depends(get_db)):

    if not db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")

    user = db.query(User).filter(User.username == user_data.username).first()
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")


@router.post("/me", response_model=UserResponse , status_code=status.HTTP_200_OK)
def me(current_user: User = Depends(current_user)):
    return current_user