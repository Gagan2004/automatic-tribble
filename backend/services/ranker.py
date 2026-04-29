from typing import List, Dict
from database.models import QueryIntent
import numpy as np

def calculate_score(product: Dict, intent: QueryIntent, retriever_score: float) -> float:
    rating_score = product.get("rating", 0) / 5.0
    review_count_norm = min(product.get("review_count", 0) / 2000.0, 1.0)
    
    price_match = 0.5
    price = product.get("price", 0)
    if intent.budget:
        if price <= intent.budget: price_match = 1.0
        else: price_match = max(0, 1.0 - (abs(intent.budget - price) / intent.budget))
            
    tag_match = 0
    tags = product.get("intent_tags", []) + product.get("feature_tags", [])
    if intent.tone and intent.tone.lower() in [t.lower() for t in tags]:
        tag_match = 1.0
            
    score = (retriever_score * 0.5) + (rating_score * 0.2) + (review_count_norm * 0.1) + (price_match * 0.1) + (tag_match * 0.1)
    return score

async def rank_products(products: List[Dict], intent: QueryIntent, retriever_scores: List[float]) -> List[Dict]:
    scored_products = []
    for i, p in enumerate(products):
        score = calculate_score(p, intent, retriever_scores[i])
        p["search_score"] = score
        scored_products.append(p)
    scored_products.sort(key=lambda x: x["search_score"], reverse=True)
    return scored_products[:10]
