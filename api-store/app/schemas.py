from pydantic import BaseModel, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)
