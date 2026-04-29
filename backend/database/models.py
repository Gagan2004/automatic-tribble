from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional

class Product(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str
    name: str
    category: str
    sub_category: str
    price: float
    currency: str = "AED"
    age_min_months: int
    age_max_months: int
    development_stage: str
    intent_tags: List[str] = []
    occasion_tags: List[str] = []
    safety_tags: List[str] = []
    feature_tags: List[str] = []
    gift_score: float = 0.0
    rating: float = 0.0
    review_count: int = 0
    popularity_score: int = 0
    description: str
    key_benefits: List[str] = []
    use_cases: List[str] = []
    parent_pain_points_solved: List[str] = []
    search_keywords: List[str] = []
    embedding_text: Optional[str] = None
    in_stock: bool = True

class QueryIntent(BaseModel):
    age_months: Optional[int] = None
    budget: Optional[float] = None
    currency: str = "AED"
    intent: str = "gift"
    tone: str = "thoughtful"
    category: Optional[str] = None

class Recommendation(BaseModel):
    id: str
    name: str
    price: float
    reason_en: str
    reason_ar: str

class RecommendRequest(BaseModel):
    query: str

class RecommendResponse(BaseModel):
    recommendations: List[Recommendation]

class ParseResponse(BaseModel):
    intent: QueryIntent
