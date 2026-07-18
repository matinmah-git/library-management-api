from datetime import datetime

from pydantic import BaseModel, ConfigDict

class LoanCreate(BaseModel):
    book_id: int
    due_day: datetime

class LoanResponse(BaseModel):
    id: str
    user_id: int
    book_id: int
    borrow_date: datetime
    due_day: datetime
    return_date: datetime | None
    returned: bool

    model_config = ConfigDict(from_attributes=True)