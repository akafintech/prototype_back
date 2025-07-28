from sqlalchemy.orm import Session
from app.model.domain.review import Review
from app.model.schema.review import ReviewCreate


def get_review(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()

def get_reviews_by_store(db: Session, store_id: int):
    return db.query(Review).filter(Review.store_id == store_id).all()

def get_reviews_by_user(db: Session, user_id: int):
    return db.query(Review).filter(Review.user_id == user_id).all()

def get_reviews_by_rating(db: Session, rating: int):
    return db.query(Review).filter(Review.rating == rating).all()

def create_review(db: Session, review: ReviewCreate):
    db_review = Review(**review.model_dump())
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review