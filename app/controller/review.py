from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.schema.review import ReviewUpdate,ResponseReview, ReviewCreate
from app.crud.review import (get_reviews_by_store,get_reviews_by_store_names,
                             get_reviews as get_reviews_crud,
                             create_review as create_review_crud,
                            update_review as update_review_crud,    
                             delete_review as delete_review_crud )
from app.crud.store import get_store_by_name,get_stores_all
from app.crud.user import get_user_by_email
from app.core.auth import verify_token

review_router = APIRouter()
security = HTTPBearer()

@review_router.get("/list/{store}", response_model=list[ResponseReview])
def get_reviews(store:str,
                offset: int = 0,
                limit: int = 10,
                credentials: HTTPAuthorizationCredentials = Depends(security),
                db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = get_user_by_email(db, email=email)
    if store == "전체":
        stores = get_stores_all(db)
        names = [store.name for store in stores]
        reviews = get_reviews_by_store_names(db, names, limit=limit, offset=offset)
    else:
        db_store = get_store_by_name(db, store)
        if not db_store:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Store not found"
            )
        reviews = get_reviews_by_store(db, db_store.id)
    res_reviews = []
    for review in reviews:
        res_review = ResponseReview(
            id=review.id,
            content=review.content,
            rating=review.rating,
            reviewer=review.reviewer,
            store=review.store.name,
            reply=review.reply,
            created_at=review.created_at.isoformat(),
            updated_at=review.updated_at.isoformat() if review.updated_at else None
        )
        res_reviews.append(res_review)
    return res_reviews

@review_router.post("/create", response_model=ResponseReview)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    store = get_store_by_name(db, review.store)
    db_review = create_review_crud(db, review, store_id=store.id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review"
        )
    res_review = ResponseReview(
        id=db_review.id,
        content=db_review.content,
        rating=db_review.rating,
        reviewer=db_review.reviewer,
        store=store.name,
        reply=db_review.reply,
        created_at=db_review.created_at.isoformat(),
        updated_at=db_review.updated_at.isoformat() if db_review.updated_at else None
    )
    return res_review

@review_router.put("/update/{review_id}", response_model=ResponseReview)
def update_review(review_id: int, review: ReviewUpdate,
                  credentials: HTTPAuthorizationCredentials = Depends(security),
                  db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_review = update_review_crud(db, review_id, review)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create review"
        )
    res_review = ResponseReview(
        id=db_review.id,
        content=db_review.content,
        rating=db_review.rating,
        reviewer=db_review.reviewer,
        store=db_review.store.name,
        reply=db_review.reply,
        created_at=db_review.created_at.isoformat(),
        updated_at=db_review.updated_at.isoformat() if db_review.updated_at else None
    )
    return res_review

@review_router.delete("/delete/{review_id}")
def delete_review(review_id: int,
                  credentials: HTTPAuthorizationCredentials = Depends(security),
                  db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    review = delete_review_crud(db, review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    return {"detail": "Review deleted successfully"}