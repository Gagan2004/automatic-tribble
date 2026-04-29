import sys
import os
import asyncio

# Ensure the local backend directory is prioritized
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

from services.retriever import retriever
from database.mongodb import get_db

async def main():
    print("Initializing Mama AI Indexer...")
    db = get_db()
    collection = db["products"]
    print(f"Loading products from {collection.__class__.__name__}...")
    await retriever.build_index(collection)
    print("Success: FAISS index is ready.")

if __name__ == "__main__":
    asyncio.run(main())
