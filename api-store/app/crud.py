import sqlalchemy
from sqlalchemy.orm import Session
from app import models, schemas


# def create_purchase(db: Session, item: schemas.Purchase):
#     db_purchase = models.PurchaseModel(**item.dict())
#     db.add(db_purchase)
#     db.commit()
#     db.refresh(db_purchase)
#     return db_purchase


def create_many_purchases(db: Session, purchase_items: list[schemas.Purchase]):
    purchase_objs = [
        models.PurchaseModel(**purchase_schema.dict())
        for purchase_schema in purchase_items
    ]
    db.bulk_save_objects(purchase_objs)
    db.commit()
    return purchase_objs


def get_purchase(db: Session, purchase_id: int):
    return (
        db.query(models.PurchaseModel)
        .filter(models.PurchaseModel.id == purchase_id)
        .first()
    )


def get_all_purchases(db: Session):
    return db.query(models.PurchaseModel).all()


def get_most_expensive_purchase(db: Session):
    return (
        db.query(models.PurchaseModel)
        .order_by(models.PurchaseModel.price.desc())
        .first()
    )


def get_total_book_count(db: Session):
    return db.query(models.PurchaseModel).count()


def get_user_books(db: Session, user_id: int):
    return (
        db.query(models.PurchaseModel)
        .filter(models.PurchaseModel.user_id == user_id)
        .all()
    )


def get_user_books_by_date(db: Session, user_id: int, date: str):
    return (
        db.query(models.PurchaseModel)
        .filter(
            models.PurchaseModel.user_id == user_id,
            models.PurchaseModel.create_at == date,
        )
        .all()
    )


def get_most_popular_day(db: Session):
    return (
        db.query(
            models.PurchaseModel.create_at,
            sqlalchemy.func.count(models.PurchaseModel.id),
        )
        .group_by(models.PurchaseModel.create_at)
        .order_by(sqlalchemy.func.count(models.PurchaseModel.id).desc())
        .first()
    )


def get_sales_by_book_and_day(db: Session, date: str):
    return (
        db.query(models.PurchaseModel)
        .filter(models.PurchaseModel.create_at == date)
        .all()
    )
