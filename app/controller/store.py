from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.model.schema.store import StoreCreate, Store
from app.crud.store import get_store_by_name,create_store as create_store_crud

store_router = APIRouter()

@store_router.get("/stores/{store_name}", response_model=Store)
def get_store(store_name: str, db: Session = Depends(get_db)):
    store = get_store_by_name(db, store_name)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Store not found"
        )
    return store

@store_router.post("/create", response_model=Store)
def create_store(store: StoreCreate, db: Session = Depends(get_db)):    
    # Check if store name already exists
    existing_store = db.query(Store).filter(Store.name == store.name).first()
    if existing_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Store name already exists"
        )
    # Create new store
    new_store = create_store_crud(db, store)
    if not new_store:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create store"
        )
    
    return new_store