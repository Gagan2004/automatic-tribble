import os
import json
import re
import requests
import google.generativeai as genai
from ollama import AsyncClient
from dotenv import load_dotenv
from database.models import QueryIntent

load_dotenv()

# Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "google/gemini-2.0-flash-001")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1:8b")

def get_best_model():
    if not GEMINI_API_KEY: return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        for pref in ['models/gemini-1.5-flash', 'models/gemini-pro']:
            if pref in models: return pref
        return models[0] if models else 'gemini-pro'
    except Exception: return 'gemini-pro'

BEST_MODEL = get_best_model()
gemini_model = genai.GenerativeModel(BEST_MODEL) if BEST_MODEL else None
ollama_client = AsyncClient(host=OLLAMA_BASE_URL, timeout=30.0)

async def parse_query(query: str) -> QueryIntent:
    prompt = f"Parse parenting query into JSON: '{query}'. Fields: age_months, budget, currency, intent, tone, category."
    
    # 1. PRIMARY: OpenRouter
    if OPENROUTER_API_KEY:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
                data=json.dumps({
                    "model": OPENROUTER_MODEL,
                    "messages": [{"role": "user", "content": prompt}]
                }),
                timeout=10
            )
            response.raise_for_status()
            text = response.json()['choices'][0]['message']['content']
            return _clean_json_to_intent(text)
        except Exception: pass

    # 2. SECONDARY: Ollama
    try:
        response = await ollama_client.generate(model=OLLAMA_MODEL, prompt=prompt, format='json')
        return _clean_json_to_intent(response.get('response', ''))
    except Exception: pass

    # 3. TERTIARY: Gemini
    if gemini_model:
        try:
            response = gemini_model.generate_content(prompt)
            return _clean_json_to_intent(response.text)
        except Exception: pass

    return _mock_parse(query)

def _clean_json_to_intent(text: str) -> QueryIntent:
    try:
        text = text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text: text = text.split("```")[1].split("```")[0].strip()
        return QueryIntent(**json.loads(text))
    except Exception: return QueryIntent()

def _mock_parse(query: str) -> QueryIntent:
    age_match = re.search(r'(\d+)\s*(month|year)', query.lower())
    age = (int(age_match.group(1)) * 12 if 'year' in age_match.group(2) else int(age_match.group(1))) if age_match else None
    budget_match = re.search(r'(under|below|around)\s*(\d+)', query.lower())
    budget = float(budget_match.group(2)) if budget_match else None
    return QueryIntent(age_months=age, budget=budget)
