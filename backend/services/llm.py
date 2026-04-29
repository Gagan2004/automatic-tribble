import os
import json
import requests
import google.generativeai as genai
from ollama import AsyncClient
from dotenv import load_dotenv
from typing import List, Dict

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

# Adaptive Gemini Model Discovery (Fallback)
def get_best_gen_model():
    if not GEMINI_API_KEY: return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for pref in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if pref in models: return pref
        return models[0] if models else 'gemini-pro'
    except Exception: return 'gemini-pro'

BEST_MODEL_NAME = get_best_gen_model()
gemini_model = genai.GenerativeModel(BEST_MODEL_NAME) if BEST_MODEL_NAME else None
ollama_client = AsyncClient(host=OLLAMA_BASE_URL, timeout=120.0)

async def generate_reasoning(products: List[Dict], query: str, intent: Dict) -> List[Dict]:
    product_context = []
    for p in products:
        product_context.append({
            'id': str(p.get('id') or p.get('_id')),
            'name': p.get('name', 'Product'),
            'benefits': p.get('key_benefits', [])[:3],
            'pain_points': p.get('parent_pain_points_solved', [])[:3]
        })

    prompt = f"Explain why these match '{query}': {json.dumps(product_context)}. Return JSON list with id, name, reason_en, reason_ar."

    # 1. PRIMARY: OpenRouter
    if OPENROUTER_API_KEY:
        print(f"Mama AI: Querying OpenRouter ({OPENROUTER_MODEL})...")
        result = await _generate_with_openrouter(prompt, products)
        if result and _is_not_fallback(result): return result

    # 2. SECONDARY: Ollama
    print(f"Mama AI: Querying Ollama SDK ({OLLAMA_MODEL})...")
    result = await _generate_with_ollama_sdk(prompt, products)
    if result and _is_not_fallback(result): return result

    # 3. TERTIARY: Native Gemini
    if gemini_model:
        print(f"Mama AI: Falling back to Native Gemini ({BEST_MODEL_NAME})...")
        return await _generate_with_gemini(prompt, products)
            
    return _get_fallback_reasoning(products)

async def _generate_with_openrouter(prompt: str, products: List[Dict]) -> List[Dict]:
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "https://mama-ai.local",
                "X-OpenRouter-Title": "Mama AI",
            },
            data=json.dumps({
                "model": OPENROUTER_MODEL,
                "messages": [{"role": "user", "content": prompt}]
            }),
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        text = data['choices'][0]['message']['content']
        return _parse_json_response(text, products)
    except Exception as e:
        print(f"OpenRouter Error: {e}")
        return None

async def _generate_with_ollama_sdk(prompt: str, products: List[Dict]) -> List[Dict]:
    try:
        response = await ollama_client.generate(model=OLLAMA_MODEL, prompt=prompt, format='json')
        return _parse_json_response(response.get('response', ''), products)
    except Exception as e:
        print(f"Ollama SDK Error: {e}")
        return None

async def _generate_with_gemini(prompt: str, products: List[Dict]) -> List[Dict]:
    try:
        response = gemini_model.generate_content(prompt)
        return _parse_json_response(response.text, products)
    except Exception as e:
        print(f"Gemini error: {e}")
        return _get_fallback_reasoning(products)

def _is_not_fallback(result: List[Dict]) -> bool:
    if not result: return False
    return result[0].get("reason_en") != "Top-rated choice based on your parenting goals."

def _parse_json_response(text: str, products: List[Dict]) -> List[Dict]:
    try:
        text = text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
        data = json.loads(text)
        return data if isinstance(data, list) else _get_fallback_reasoning(products)
    except Exception: return _get_fallback_reasoning(products)

def _get_fallback_reasoning(products: List[Dict]) -> List[Dict]:
    return [{"id": str(p.get("id") or p.get("_id")), "name": p.get("name", "Product"), "reason_en": "Top-rated choice based on your parenting goals.", "reason_ar": "خيار ممتاز يعتمد على أهدافك التربوية."} for p in products]
