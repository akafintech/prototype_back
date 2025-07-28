from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.schema.review import ReviewBase
from app.crud.review import get_reviews_by_user

review_router = APIRouter()

@review_router.get("/")
def get_reviews(user_id:int,db: Session = Depends(get_db)):
    reviews = get_reviews_by_user(db, user_id=user_id)

    return reviews

@review_router.post("/create", response_model=ReviewBase)
def create_review(review: ReviewBase, db: Session = Depends(get_db)):
    db.add(review)
    db.commit()
    db.refresh(review)
    return review