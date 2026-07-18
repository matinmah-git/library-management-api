from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import require_roles
from app.database.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.user import MessageResponse


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryResponse])
def get_categories( db: Session = Depends(get_db)):

    return db.query(Category).all()


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            ADMIN,
            LIBRARIAN,
        )
    ),
):
    existing_category = (
        db.query(Category)
        .filter(Category.name == category_data.name)
        .first()
    )

    if existing_category:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists.",
        )

    category = Category(
        name=category_data.name,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(
            ADMIN,
            LIBRARIAN,
        )
    ),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    update_data = category_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)

    return category


@router.delete(
    "/{category_id}",
    response_model=MessageResponse,
)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_roles(ADMIN)
    ),
):
    category = (
        db.query(Category)
        .filter(Category.id == category_id)
        .first()
    )

    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    db.delete(category)
    db.commit()

    return MessageResponse(
        message="Category deleted successfully."
    )