from sqlalchemy import Column, Integer, String, DateTime,ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base
from sqlalchemy.orm import relationship  # 추가


class Review(Base):
    __tablename__ = "tb_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    picture = Column(String, nullable=True)  
    store_id = Column(Integer, ForeignKey("tb_store.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("tb_user.id"), nullable=False)

    store = relationship("Store", back_populates="review")
    user = relationship("User", back_populates="review")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())