# 📊 GFG — AI Business Intelligence Platform

An AI-powered Business Intelligence platform that lets users explore and understand business data through natural conversation. Built with **FastAPI**, **LangGraph**, and a **React** frontend.

---

## 🏗️ Architecture Overview

```
gfg/
├── api/
│   └── main.py              # FastAPI server (REST endpoints)
├── agent/
│   ├── workflow.py           # LangGraph chatbot (AI agent logic)
│   └── tools/
│       └── sql_generator.py  # Tool: converts natural language → SQL
├── frontend/                 # React app (Chart.js visualisations)
├── .env                      # Environment variables (API keys)
├── requirements.txt          # Python dependencies (pinned)
├── pyproject.toml            # Project metadata (uv / pip)
└── README.md
```

---

## 🚀 Running the FastAPI Server

### Prerequisites

| Tool | Version | Check |
|------|---------|-------|
| **Python** | ≥ 3.13 | `python --version` |
| **pip** or **uv** | latest | `pip --version` / `uv --version` |
| **Git** | any | `git --version` |

> You also need an **OpenAI API key** for the AI agent to work.

---

### 1. Clone the Repository

```bash
git clone https://github.com/debangshu919/gfg.git
cd gfg
```

---

### 2. Create & Activate a Virtual Environment

#### Using `venv` (built-in)

```bash
# Create
python -m venv .venv

# Activate (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate (Windows CMD)
.\.venv\Scripts\activate.bat

# Activate (macOS / Linux)
source .venv/bin/activate
```

#### Or using `uv` (faster alternative)

```bash
uv venv
# then activate the .venv as shown above
```

---

### 3. Install Dependencies

#### Using `pip`

```bash
pip install -r requirements.txt
```

#### Or using `uv`

```bash
uv sync
```

This installs everything the server needs: **FastAPI**, **Uvicorn**, **LangChain/LangGraph**, **psycopg2-binary**, **python-dotenv**, and more.

---

### 4. Set Up Environment Variables

Create a `.env` file in the project root (if it doesn't already exist):

```bash
# .env
OPENAI_API_KEY=sk-proj-your-openai-api-key-here
```

> ⚠️ **Never commit your `.env` file.** It is already in `.gitignore`.

---

### 5. Start the FastAPI Server

```bash
uvicorn api.main:app --reload
```

You should see output like:

```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process ...
INFO:     Started server process ...
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

| Option | Description |
|--------|-------------|
| `--reload` | Auto-restart on code changes (dev mode) |
| `--host 0.0.0.0` | Expose to other devices on the network |
| `--port 8080` | Change the port (default is `8000`) |

**Example — run on all interfaces at port 8080:**

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8080
```

---

### 6. Verify the Server is Running

Open your browser or use `curl`:

```bash
curl http://127.0.0.1:8000/
```

**Expected response:**

```json
{
  "success": true,
  "message": "API is running"
}
```

---

## 📡 API Endpoints

### `GET /`  — Health Check

Returns the server status.

```bash
curl http://127.0.0.1:8000/
```

### `POST /chat` — Chat with the AI Agent

Send a natural-language message. The AI decides whether to respond conversationally or query the database.

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the total revenue?"}'
```

**Response (data query):**

```json
{
  "success": true,
  "type": "data",
  "prompt": "What is the total revenue?",
  "response": "The total revenue across all regions is ...",
  "sql_query": "SELECT SUM(revenue) FROM sales;",
  "chart_type": "bar",
  "x_axis": "region",
  "y_axis": "revenue",
  "data": [{ "region": "East", "revenue": 50000 }]
}
```

**Response (conversational):**

```json
{
  "success": true,
  "type": "chat",
  "prompt": "Hello!",
  "response": "Hello! I'm your AI Business Intelligence Analyst. How can I help you today?"
}
```

---

## 🖥️ Running the Frontend (Optional)

The React frontend lives in the `frontend/` directory:

```bash
cd frontend
npm install
npm start
```

This starts the React dev server on `http://localhost:3000` and communicates with the FastAPI backend at `http://localhost:8000`.

---

## 📝 License

This project was built for the GFG Hackathon.