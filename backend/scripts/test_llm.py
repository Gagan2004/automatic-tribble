import sys
import os
import asyncio
import json

# Add backend to path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, backend_path)

from services.llm import generate_reasoning

async def test():
    print("Testing LLM Reasoning...")
    products = [
        {
            "id": "prod_001",
            "name": "Lite Humidifier",
            "description": "Quiet humidifier for better sleep.",
            "key_benefits": ["Quiet operation", "Adjustable mist"],
            "parent_pain_points_solved": ["Dry air", "Restless nights"]
        }
    ]
    query = "help my baby sleep better in dry weather"
    intent = {"age_months": 6, "intent": "necessity"}
    
    results = await generate_reasoning(products, query, intent)
    print("\nResults:")
    print(json.dumps(results, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test())
