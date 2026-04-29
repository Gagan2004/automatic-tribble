import sys
import os
import asyncio

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

from services.retriever import retriever
from database.mongodb import get_db

async def test():
    print("Loading index...")
    db = get_db()
    collection = db["products"]
    # We need to build it once in memory to populate _all_products and tfidf for the instance
    await retriever.build_index(collection)
    
    queries = [
        "teething baby pain relief",
        "thoughtful gift for 1 year old under 300",
        "messy mealtime solution"
    ]
    
    for q in queries:
        print(f"\nQuery: {q}")
        results = await retriever.search(q, k=3)
        for pid, score in results:
            product = retriever._all_products.get(pid)
            print(f"- {product['name']} (Score: {score:.4f})")

if __name__ == "__main__":
    asyncio.run(test())
