from pydantic import BaseModel, ConfigDict


class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    description: str | None = None
    published_year: int | None = None
    total_copies: int
    available_copies: int
    category_id: int


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    isbn: str | None = None
    description: str | None = None
    published_year: int | None = None
    total_copies: int | None = None
    available_copies: int | None = None
    category_id: int | None = None


class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes=True)