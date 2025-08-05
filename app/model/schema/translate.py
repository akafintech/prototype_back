from pydantic import BaseModel

class TranslateReviewBase(BaseModel):
    text: str
    target_language: str
