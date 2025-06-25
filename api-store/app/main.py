import sqlalchemy
import uvicorn
from fastapi import Request, status, FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, create_tables
create_tables()
app = FastAPI()
@app.get("/")
def health_check():
    return {"service": "API Store", "status": "healthy"}
def get_db():
    try:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        yield None
@app.exception_handler(ValidationError)
def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )
@app.post("/purchases/", response_model=list[schemas.Purchase])
def create_purchase(purchases: list[schemas.Purchase], db: Session = Depends(get_db)):
    purchase = crud.create_many_purchases(db=db, purchase_items=purchases)
    print("\n\n CREATED")
    return purchase
@app.get("/purchases/{purchase_id}")
def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = crud.get_purchase(db, purchase_id)
    if not purchase:
        return JSONResponse(content={"message": "Purchase not found."}, status_code=404)
    return purchase
@app.get("/purchases")
def get_all_purchases(db: Session = Depends(get_db)):
    purchases = crud.get_all_purchases(db)
    return purchases
@app.get("/purchases/most-expensive/")
def get_most_expensive_purchase(db: Session = Depends(get_db)):
    purchase = crud.get_most_expensive_purchase(db)
    return purchase
@app.get("/purchases/total-count/")
def get_total_book_count(db: Session = Depends(get_db)):
    count = crud.get_total_book_count(db)
    return {"count": count}
@app.get("/purchases/user/{user_id}")
def get_user_books(user_id: int, db: Session = Depends(get_db)):
    purchases = crud.get_user_books(db, user_id)
    return purchases
@app.get("/purchases/user/{user_id}/date/{date}")
def get_user_books_by_date(user_id: int, date: str, db: Session = Depends(get_db)):
    purchases = crud.get_user_books_by_date(db, user_id, date)
    return purchases
@app.get("/most-popular-day")
def get_most_popular_day(db: Session = Depends(get_db)):
    date, count = crud.get_most_popular_day(db)
    return {"date": date, "count": date}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
