import asyncio
from ollama import AsyncClient
import os
import json
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

async def test_sdk():
    print(f"DEBUG: Attempting connection to {OLLAMA_BASE_URL}")
    client = AsyncClient(host=OLLAMA_BASE_URL)
    
    try:
        # Step 1: List models
        print("STEP 1: Listing models...")
        models_resp = await client.list()
        available = [m.get('model') or m.get('name') for m in models_resp.get('models', [])]
        print(f"SUCCESS: Found models: {available}")
        
        # Step 2: Simple generate
        print(f"STEP 2: Testing generation with {OLLAMA_MODEL}...")
        response = await client.generate(
            model=OLLAMA_MODEL,
            prompt="hi",
            format='json'
        )
        print("SUCCESS: SDK generated response.")
        print(f"RESPONSE: {response.get('response')}")
        
    except Exception as e:
        print(f"FAILURE: SDK Error type: {type(e).__name__}")
        print(f"FAILURE: SDK Error message: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_sdk())
