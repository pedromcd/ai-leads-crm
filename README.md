**English** | [Português](README.pt-BR.md)

# 🤖 AI Leads CRM

**An automated lead-qualification pipeline: an n8n workflow sends each incoming lead to an LLM via OpenRouter, turns the answer into structured data, and a FastAPI backend validates and stores it in SQLite.**

The goal is to show how a language model fits into a **real business flow**, not as an isolated chatbot, but as one step in a pipeline with orchestration, validation, persistence, and reporting.

---

## 🎯 Problem and goal

Small businesses receive leads through forms, WhatsApp, and social media, and someone has to read each message to decide: *What does this person want? How urgent is it? What should we reply?* That triage is repetitive and easy to delay.

This project automates the first triage:

1. a lead arrives through a **webhook**;
2. an **LLM** classifies the intent, assigns a priority and a 0–100 score, suggests the next action, and drafts a reply;
3. the result is **validated** and **stored**, so the team can act on the highest-priority leads first and analyze the funnel later.

---

## ⚙️ How it works

```text
POST /webhook/lead  (name, email, phone, source, message)
        │
        ▼
┌────────────────────────── n8n workflow ───────────────────────────┐
│ 1. Webhook          receives the lead                             │
│ 2. Edit Fields      normalizes the input fields                   │
│ 3. OpenRouter       calls mistralai/mistral-7b-instruct           │
│                     (system prompt requires JSON only)            │
│ 4. Code (JS)        strips Markdown code fences, parses JSON,     │
│                     falls back to safe defaults if parsing fails, │
│                     and merges the AI fields with the lead data   │
│ 5. HTTP Request     POST to the FastAPI backend                   │
│ 6. Respond          {"ok": true, "lead_saved": true}              │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
FastAPI  POST /lead  → Pydantic validation → score clamped to 0–100 → SQLite
        │
        ▼
GET /leads (latest leads)   ·   report.py (totals by intent and priority, average score)
```

### What the model returns

The system prompt constrains the output to a fixed schema with closed label sets:

| Field | Allowed values |
|---|---|
| `intent` | `Pricing`, `Trial`, `Support`, `General`, `Partnership` |
| `priority` | `Low`, `Medium`, `High`, `Urgent` |
| `score` | integer from 0 to 100 |
| `next_action` | short text |
| `suggested_reply` | short WhatsApp-style reply, in Portuguese |

Illustrative example of a stored lead:

```json
{
  "id": "3f9a1c2e",
  "created_at": "2026-09-25T14:32:10",
  "name": "Ana",
  "source": "instagram",
  "message": "Hi! How much is the annual plan for 5 users?",
  "intent": "Pricing",
  "priority": "High",
  "score": 82,
  "next_action": "Send the annual pricing table",
  "suggested_reply": "Oi, Ana! Te envio agora os valores do plano anual para 5 usuários 😊",
  "status": "NEW"
}
```

---

## 🧱 Engineering decisions

- **Orchestration separate from the backend.** n8n handles the flow (receiving the lead, calling the model, routing the result); FastAPI only owns validation and persistence. Each piece can change without breaking the other.
- **Never trust the model's output blindly.** LLMs sometimes wrap JSON in Markdown or return invalid JSON. The Code node cleans the response and, if parsing still fails, falls back to neutral defaults (`General`, `Medium`, `50`) so the lead is never lost.
- **A second validation layer in the API.** Pydantic rejects payloads with missing or wrongly typed fields, and the score is clamped to 0–100 before being written.
- **Closed label sets.** Restricting `intent` and `priority` to fixed values makes the data aggregatable (reports, dashboards) instead of free text.
- **Low temperature (0.3)** for more consistent classifications.

---

## 🛠️ Tech stack

- **n8n** (Docker): workflow orchestration
- **OpenRouter** + **Mistral 7B Instruct**: LLM classification
- **Python**, **FastAPI**, **Pydantic**, **Uvicorn**: API and validation
- **SQLite**: storage
- **JavaScript**: response parsing inside n8n

---

## 🔌 API

| Method | Route | Description |
|---|---|---|
| `GET` | `/health` | Health check; also returns the database path |
| `POST` | `/lead` | Validates and stores an analyzed lead; returns its `lead_id` |
| `GET` | `/leads?limit=50` | Lists the latest leads, newest first |

Interactive documentation is available at `http://localhost:8000/docs` (FastAPI Swagger UI).

---

## ▶️ Running locally

### 1. Backend

```bash
git clone https://github.com/pedromcd/ai-leads-crm.git
cd ai-leads-crm/python
pip install fastapi uvicorn pydantic
uvicorn app:app --reload --port 8000
```

The database is created automatically at `../data/leads.db`. To use another location, set the `DB_PATH` environment variable.

### 2. n8n

```bash
cd ../n8n
docker compose up -d
```

Open `http://localhost:5678` (the compose file enables basic auth with local development credentials; change them before exposing n8n anywhere).

### 3. Import the workflow

1. In n8n, import `n8n/n8n-ai-leads-crm-workflow.json`.
2. In the **OpenRouter** node, set the `Authorization` header to `Bearer <your OpenRouter API key>`. No key is stored in this repository.
3. Activate the workflow. The **HTTP Request** node already points to `http://host.docker.internal:8000/lead`, the backend running on your machine.

### 4. Send a test lead

```bash
curl -X POST http://localhost:5678/webhook/lead \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana","email":"ana@example.com","source":"instagram","message":"Quanto custa o plano anual para 5 usuários?"}'
```

Then check the result:

```bash
curl http://localhost:8000/leads
cd python && python report.py
```

---

## 🧩 Structure

```text
ai-leads-crm/
├── n8n/
│   ├── docker-compose.yml                  # Local n8n instance
│   └── n8n-ai-leads-crm-workflow.json      # Exported workflow (no credentials)
├── python/
│   ├── app.py                              # FastAPI: /health, /lead, /leads
│   └── report.py                           # Totals by intent/priority and average score
└── data/                                   # SQLite database (created at runtime)
```

---

## 🚧 Next steps

- **Evaluate the classifier:** build a small labeled set of leads and measure intent accuracy, priority consistency, and the rate of malformed JSON, then compare models and prompt versions.
- Use OpenRouter's **structured outputs / JSON schema** mode instead of relying only on the prompt.
- Add a `requirements.txt`, Docker for the backend, and automated tests.
- Add an endpoint to update the lead `status` (NEW → CONTACTED → WON/LOST) and a simple dashboard.

---

## 👨‍💻 Author

**Pedro Marques Correa Domingues** · [GitHub](https://github.com/pedromcd) · [Portfolio](https://pedromcd.github.io)
