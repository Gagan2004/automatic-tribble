# Mama AI: Hybrid Parenting Assistant 🎠

Mama AI is a high-performance, local-first parenting recommendation engine. It combines semantic vector search with multiple AI providers (OpenRouter, Ollama, and Gemini) to provide empathetic, developmentally-aware product advice.

## 🚀 Features
- **Adaptive UI**: A premium dark-mode interface with glassmorphism and motion-sensing search.
- **Local-First AI**: Prioritizes local Ollama (`llama3.1:8b`) for privacy and zero-cost inference.
- **Triple-Tier Resilience**: Automated failover between OpenRouter, Ollama, and Native Gemini.
- **Semantic Search**: Uses FAISS vector indexing to match queries like *"11 month old can't sleep"* to practical solutions.
- **Bilingual Support**: Full English and Arabic support for all reasoning and interface elements.

## 🛠️ Tech Stack
- **Frontend**: React, Tailwind CSS, Lucide Icons.
- **Backend**: FastAPI, Pydantic V2.
- **AI/ML**: FAISS (Vector Indexing), Scikit-learn (TF-IDF Fallback).
- **Database**: MongoDB (via Motor) with JSON-mocked resilience.

## 📦 Setup

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev
```

### 3. Environment
Create a `.env` in the root:
```env
OPENROUTER_API_KEY=your_key
GEMINI_API_KEY=your_key
OLLAMA_MODEL=llama3.1:8b
```

## 📜 License
MIT
