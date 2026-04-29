from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database.mongodb import get_db, ping_db
from database.models import RecommendRequest, RecommendResponse, ParseResponse, Recommendation
from services.parser import parse_query
from services.retriever import retriever
from services.ranker import rank_products
from services.llm import generate_reasoning
from bson import ObjectId
import uvicorn

app = FastAPI(title="AI Parenting Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    db = get_db()
    collection = db["products"]
    await retriever.build_index(collection)

@app.get("/health")
async def health():
    db_ok = await ping_db()
    return {"status": "ok", "database": "connected" if db_ok else "disconnected"}

@app.post("/parse", response_model=ParseResponse)
async def parse(request: RecommendRequest):
    intent = await parse_query(request.query)
    return {"intent": intent}

@app.post("/recommend", response_model=RecommendResponse)
async def recommend(request: RecommendRequest):
    intent = await parse_query(request.query)
    search_results = await retriever.search(request.query, intent=intent, k=15)
    
    if not search_results:
        return {"recommendations": []}
        
    db = get_db()
    collection = db["products"]
    products = []
    similarities = []
    
    for pid, score in search_results:
        doc = await collection.find_one({"id": pid})
        if not doc:
            try:
                doc = await collection.find_one({"_id": ObjectId(pid)})
            except:
                doc = await collection.find_one({"_id": pid})
            
        if doc:
            doc["_id"] = str(doc.get("id") or doc.get("_id"))
            products.append(doc)
            similarities.append(score)
            
    top_products = await rank_products(products, intent, similarities)
    
    # Use model_dump() for Pydantic V2 compatibility
    reasoning_data = await generate_reasoning(top_products, request.query, intent.model_dump())
    
    recommendations = []
    for item in reasoning_data:
        prod = next((p for p in top_products if str(p.get("id") or p.get("_id")) == str(item["id"])), None)
        recommendations.append(Recommendation(
            id=str(item["id"]),
            name=item["name"],
            price=prod.get("price", 0) if prod else 0,
            reason_en=item["reason_en"],
            reason_ar=item["reason_ar"]
        ))
        
    return {"recommendations": recommendations}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
