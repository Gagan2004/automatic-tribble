import asyncio
import os
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), "backend"))

from services.retriever import retriever
from db.mongodb import get_db

async def test_retriever():
    print("Testing retriever...")
    db = get_db()
    collection = db["products"]
    
    print("Building index...")
    await retriever.build_index(collection)
    
    print("Searching...")
    query = "gift for a baby boy"
    results = await retriever.search(query, k=5)
    
    print(f"Results for '{query}':")
    for pid, dist in results:
        doc = await collection.find_one({"_id": pid})
        if not doc:
            doc = await collection.find_one({"id": pid})
        print(f" - {doc['name']} (Distance: {dist:.4f})")

if __name__ == "__main__":
    asyncio.run(test_retriever())
