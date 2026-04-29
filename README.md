###LOOM LINK:
https://www.loom.com/share/00799edcb5e44fafafc45b0336ea98c1

# Mama AI: Hybrid Parenting Assistant 🎠

 
Mama AI is a  parenting recommendation engine. It bridges the gap between ambiguity and product search, using a **Triple-Tier AI Architecture** to suggest, context-aware products from the database.

---

## ⚡ Setup and Run (< 5 Minutes)

### 1. Requirements
- **Python 3.10+** & **Node.js 18+**
- **Ollama** (optional for local-first): `ollama pull llama3.1:8b`

### 2. Quick Start
```bash
# Clone and enter
git clone https://github.com/Gagan2004/automatic-tribble.git
cd automatic-tribble

# Setup Backend
cd backend
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py

# Setup Frontend (New Terminal)
cd frontend
npm install
npm run dev
```

### 3. Environment
Rename `.env.example` (or create `.env`) in the root:
```env
{ANY 1 of three is required}

OPENROUTER_API_KEY=your_key { the project is evaluated on this} ** RECOMMENDED
GEMINI_API_KEY=your_key 
OLLAMA_MODEL=llama3.1:8b { local LLm but has to be pre-downloaded with a model llama3.1:8b}
```

---

## 📊 Evals: The Rubric & Results

### The Rubric
- **Accuracy (0-5)**: Does the product age-match and intent-match?
- **Tone (0-5)**: Is the reasoning empathetic and parenting-focused?
- **Speed (0-5)**: Does it respond in <3s (Cloud) or <15s (Local)?
- **Resilience (0-5)**: Does it gracefully handle nonsense/adversarial queries?

### Test Cases & Scores
| Query | Type | Score | Result |
| :--- | :--- | :--- | :--- |
| "11 month old can't sleep" | Easy | 5/5 | Suggested White Noise + Swaddle. |
| "Baby food for 4 months" | Easy | 5/5 | Accurate age-filtered feeding sets. |
| "Teething pain relief" | Easy | 4/5 | Good results, slightly slow fallback. |
| "Products for newly born to fight against crime" | Adversarial | 5/5 | **PASSED**: Corrected to "No Results Found". |
| "Best diaper for a fish" | Adversarial | 4/5 | **PASSED**: Rejected nonsense query. |
| "Hiking with newborn" | Intent | 5/5 | Recommended ergonomic carriers. |
| "Cheap gift < 50 AED" | Constraint | 3/5 | Matched price but some reasoning was generic. |

**Total Average Score: 4.4 / 5.0**

> [!IMPORTANT]
> **Failure Mode**: Earlier versions hallucinated crime-fighting justifications for baby nail files. This was fixed by implementing **Similarity Thresholding (0.15)** and **Explicit Rejection Prompts**.

---

## 🏗️ Trade-offs & Architecture

### Why This Problem?
I chose **Parenting Search** because I liked the problem statement of - ""Gift finder for moms. Natural-language input like “thoughtful gift for a friend with a 6-month-old, under 200 AED” ""...But I wanted to build more on this ...so this project does not only deals with gifts but matches any parenting concerns/ambiguity to an right product .. 

ex-  a concerned parent seraches - "baby can't sleep a night" maps to white noise emulator or similar products for the baby ...



### The Triple-Tier Choice
 Rejected a "Cloud-Only" approach (too expensive/rate-limited) and a "Local-Only" approach (too slow for mobile).
- **Primary**: OpenRouter (Google Gemini 2.0 Flash) — Unbeatable speed/cost.
- **Secondary**: Local Ollama (Llama 3.1 8b) — Privacy and zero-cost fallback.
- **Tertiary**: Native Gemini — Final emergency failover.

### What We Cut
- **User Authentication**: Cut to focus on the search experience.
- **NO actual  pages for products**: Simulated with "Explore Match" buttons to keep the focus on the AI.

---

## 🛠️ Tooling & Agent Collaboration

### AI Assistant: Antigravity
This project was built using **Antigravity (Google DeepMind)** in a high-intensity agentic loop.

- **Pair-Coding**: 80% of the architecture was developed through collaborative iteration. Antigravity (the agent) proposed refactors (e.g., migrating from `requests` to the `Ollama SDK`), and the user provided real-world edge cases.
- **Agentic Loops**:  used autonomous loops for UI testing, environment debugging (fixing the PowerShell `&&` vs `;` syntax), and data indexing.
- **Prompt Iteration**:  spent 3 cycles refining the "Reasoning Prompt" to stop hallucinations.

### Model Stack
- **Reasoning**: `google/gemini-2.0-flash-001` (via OpenRouter) for its 1M context and speed.
- **Local Inference**: `llama3.1:8b` (via Ollama) for robust local justifications.
- **Embeddings**: `models/text-embedding-004` (Native Gemini) for superior semantic search.

---

## 🛠️ Stack
- **Backend**: FastAPI, FAISS, Motor (MongoDB), Scikit-learn.
- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion (for zoom transitions).
- **AI Integration**: Ollama SDK, OpenRouter API, Google Generative AI.

---
**Mama AI • Built with 💜 for parents, powered by Hybrid AI.**
