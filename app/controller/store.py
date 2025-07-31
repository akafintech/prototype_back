from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.auth import verify_token
from app.core.database import get_db
from app.model.schema.store import StoreCreate, Store
from app.crud.store import (get_store,get_store_by_name,get_stores,get_store_by_business_number,
                            create_store as create_store_crud,
                            delete_store as delete_store_crud)
from app.crud.user import get_user_by_email

store_router = APIRouter()
security = HTTPBearer()

# @store_router.get("/{store_id}", response_model=Store)
# def get_store(store_id: str,
#               credentials: HTTPAuthorizationCredentials = Depends(security), 
#               db: Session = Depends(get_db)):
#     email = verify_token(credentials.credentials)
#     if email is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Could not validate credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     store = get_store(db, store_id)
#     if not store:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Store not found"
#         )
#     return store

@store_router.get("/list", response_model=list[Store])
def list_stores(credentials: HTTPAuthorizationCredentials = Depends(security), 
                db: Session = Depends(get_db)):
    email = verify_token(credentials.credentials)
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = get_user_by_email(db, email=email)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )   
    stores = get_stores(db,db_user.id)
    return stores

@store_router.post("/create", response_model=Store)
def create_store(store: StoreCreate,
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
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )    
    # Check if store name already exists
    existing_store = get_store_by_name(db, name=store.name)
    if existing_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Store name already exists"
        )
    bs_number_store = get_store_by_business_number(db, business_number=store.business_number)
    if bs_number_store:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Business number already exists"
        )
    # Create new store
    new_store = create_store_crud(db, store, db_user.id)
    if not new_store:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create store"
        )
    
    return new_store

@store_router.delete("/delete/{store_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    store = delete_store_crud(db, store_id)
    if not store:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete store or store not found"
        )
    
    return {"detail": "Store deleted successfully"}