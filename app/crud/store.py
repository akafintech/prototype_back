from sqlalchemy.orm import Session
from app.model.domain.store import Store
from app.model.schema.store import StoreCreate


def get_store(db: Session, store_id: int):
    return db.query(Store).filter(Store.id == store_id).first()

def get_store_by_name(db: Session, name: str):
    return db.query(Store).filter(Store.name == name).first()   

def create_store(db: Session, store: StoreCreate):
    db_store = Store(**store.model_dump())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store