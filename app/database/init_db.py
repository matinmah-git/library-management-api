from app.core.config import settings
from app.models.user import User
from app.core.security import hash_password
from app.database.database import sessionlocal
from sqlalchemy.orm import Session


def create_admin():
    db: Session = sessionlocal()
    try:
        admin = db.query(User).filter(User.role == "admin").first()
        if admin:
            return
        admin = User(username=settings.ADMIN_USERNAME, email=settings.ADMIN_EMAIL, hashed_password=hash_password(settings.ADMIN_PASSWORD), role="admin")
        db.add(admin)
        db.commit()

        print("Default admin created")
    finally:
        db.close()