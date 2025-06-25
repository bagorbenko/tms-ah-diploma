from sqlalchemy import MetaData, Table, Column, Integer, String, Float, DateTime
from app.database import Base
class PurchaseModel(Base):
    __tablename__ = "purchase"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    order_id = Column(Integer)
    book_id = Column(Integer)
    user_id = Column(Integer)
    book_title = Column(String)
    author_name = Column(String)
    price = Column(Float)
    create_at = Column(String)
    publisher_id = Column(Integer)
