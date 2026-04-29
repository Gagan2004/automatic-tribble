import os
import faiss
import numpy as np
import json
import google.generativeai as genai
from motor.motor_asyncio import AsyncIOMotorCollection
from database.models import Product, QueryIntent
from typing import List, Tuple
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def get_best_embed_model():
    if not GEMINI_API_KEY: return None
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        models = [m.name for m in genai.list_models() if 'embedContent' in m.supported_generation_methods]
        print(f"Retriever: Found embedding models: {models}")
        for pref in ['models/text-embedding-004', 'models/embedding-001', 'models/embedding-gecko-001']:
            if pref in models: return pref
        return models[0] if models else 'models/embedding-001'
    except Exception as e:
        print(f"Retriever: Embed model discovery failed ({e})")
        return 'models/embedding-001'

EMBED_MODEL = get_best_embed_model()
INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "embeddings", "index.faiss")
METADATA_PATH = os.path.join(os.path.dirname(__file__), "..", "embeddings", "metadata.npy")

class Retriever:
    def __init__(self):
        self.index = None
        self.product_ids = []
        self._all_products = {}
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = None

    def _get_embedding(self, text: str, task_type="retrieval_document"):
        try:
            if not EMBED_MODEL: return None
            result = genai.embed_content(model=EMBED_MODEL, content=text, task_type=task_type, title="Mama AI" if task_type == "retrieval_document" else None)
            return result['embedding']
        except Exception: return None

    def _construct_embedding_text(self, p: dict) -> str:
        return f"{p.get('name', '')} {p.get('description', '')} {' '.join(p.get('key_benefits', []))} {' '.join(p.get('parent_pain_points_solved', []))}".strip()

    async def build_index(self, collection: AsyncIOMotorCollection):
        products = []
        async for doc in collection.find({"in_stock": True}):
            products.append(doc)
            self._all_products[str(doc.get("id"))] = doc
        if not products: return
        embeddings, self.product_ids, texts = [], [], []
        print(f"Indexing {len(products)} products with {EMBED_MODEL} + TF-IDF Fallback...")
        for p in products:
            text = self._construct_embedding_text(p)
            texts.append(text)
            emb = self._get_embedding(text)
            embeddings.append(emb if emb else np.zeros(768))
            self.product_ids.append(str(p.get("id")))
        embeddings = np.array(embeddings).astype('float32')
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(embeddings)
        self.tfidf_matrix = self.tfidf.fit_transform(texts)
        os.makedirs(os.path.dirname(INDEX_PATH), exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)
        np.save(METADATA_PATH, np.array(self.product_ids))

    def load_index(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(METADATA_PATH):
            self.index = faiss.read_index(INDEX_PATH)
            self.product_ids = np.load(METADATA_PATH).tolist()
            return True
        return False

    async def search(self, query: str, intent: QueryIntent = None, k: int = 15) -> List[Tuple[str, float]]:
        if self.index is None and not self.load_index(): return []
        query_emb = self._get_embedding(query, task_type="retrieval_query")
        if query_emb:
            query_vec = np.array([query_emb]).astype('float32')
            distances, indices = self.index.search(query_vec, k * 3)
            candidates = [(self.product_ids[idx], 1.0 / (1.0 + dist)) for dist, idx in zip(distances[0], indices[0]) if idx != -1]
        else:
            print("Using TF-IDF fallback search.")
            query_tfidf = self.tfidf.transform([query])
            sims = (self.tfidf_matrix * query_tfidf.T).toarray().flatten()
            idxs = np.argsort(sims)[::-1][:k*3]
            candidates = [(self.product_ids[i], float(sims[i])) for i in idxs]
        scored = []
        for pid, base in candidates:
            p = self._all_products.get(pid)
            if not p: continue
            score = base + (p.get('popularity_score', 0) / 1000.0) + (p.get('gift_score', 0) / 10.0)
            if intent and intent.age_months is not None:
                if not (p.get('age_min_months', 0) <= intent.age_months <= p.get('age_max_months', 999)): score *= 0.1
            scored.append((pid, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

retriever = Retriever()
