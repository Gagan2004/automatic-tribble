import motor.motor_asyncio
import os
import json
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "mama_db"
JSON_DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data.json")

# Force Mock for now as we don't have MongoDB
FORCE_MOCK = True

class MockCollection:
    def __init__(self, data: List[Dict]):
        self.data = data

    async def find(self, query: Dict = None):
        # Basic mock find with in_stock filter support
        for item in self.data:
            if query and "in_stock" in query:
                if item.get("in_stock") == query["in_stock"]:
                    yield item
            else:
                yield item

    async def find_one(self, query: Dict):
        # Mock find_one by ID or _id
        pid = query.get("_id") or query.get("id")
        for item in self.data:
            if str(item.get("id")) == str(pid):
                return item
        return None

class MockDB:
    def __init__(self):
        if not os.path.exists(JSON_DB_PATH):
            print(f"Warning: JSON DB path {JSON_DB_PATH} not found.")
            self.data = []
        else:
            with open(JSON_DB_PATH, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        self.products = MockCollection(self.data)

    def __getitem__(self, name):
        if name == "products":
            return self.products
        return None

def get_db():
    if FORCE_MOCK:
        return MockDB()
    try:
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=2000)
        return client[DATABASE_NAME]
    except Exception:
        return MockDB()

async def ping_db():
    if FORCE_MOCK:
        return True
    return True # Assume OK for now
