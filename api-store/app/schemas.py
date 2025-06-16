from pydantic import BaseModel
from datetime import datetime


class Purchase(BaseModel):
    order_id: int
    book_id: int
    user_id: int
    book_title: str
    author_name: str
    price: float
    create_at: str
    publisher_id: int

    class Config:
        orm_mode = True
