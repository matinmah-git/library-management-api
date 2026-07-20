from datetime import datetime

from pydantic import BaseModel, ConfigDict

class LoanCreate(BaseModel):
    book_id: int
    due_date: datetime

class LoanResponse(BaseModel):
    id: int
    user_id: int
    book_id: int
    borrow_date: datetime
    due_date: datetime
    return_date: datetime | None
    returned: bool

    model_config = ConfigDict(from_attributes=True)