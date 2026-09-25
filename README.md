# AI Leads CRM

**LLM-powered lead qualification pipeline using n8n, FastAPI, OpenRouter, and SQLite.**

This project demonstrates how a language model can be integrated into an end-to-end business workflow instead of being used as an isolated chatbot. Incoming leads are processed by an automated pipeline, converted into structured AI outputs, validated by a backend API, and persisted for later analysis.

## System flow

```text
Inbound lead
    ↓
n8n webhook
    ↓
LLM classification via OpenRouter
    ↓
Structured JSON output
    ↓
FastAPI validation
    ↓
SQLite persistence
    ↓
Reporting / downstream actions
```

The AI step produces structured fields such as:

```json
{
  "intent": "...",
  "priority": "...",
  "score": 0,
  "next_action": "...",
  "suggested_reply": "..."
}
```

## What the system does

- receives leads through an n8n webhook;
- classifies lead intent with an LLM;
- assigns priority;
- produces a score from 0 to 100;
- proposes the next action;
- generates a suggested reply;
- validates the structured payload with Pydantic/FastAPI;
- persists the result in SQLite;
- exposes API endpoints to inspect stored leads;
- provides a reporting script for basic analysis.

## Backend model

The FastAPI backend validates the lead payload before storage:

```python
class Lead(BaseModel):
    name: str
    email: Optional[str] = ""
    phone: Optional[str] = ""
    source: Optional[str] = "web"
    message: str
    intent: str
    priority: str
    score: int
    next_action: str
    suggested_reply: str
```

The score is normalized to the accepted 0–100 range before persistence.

## API

### Health check

```http
GET /health
```

### Store an analyzed lead

```http
POST /lead
```

### List recent leads

```http
GET /leads
```

## Tech stack

- **Python**
- **FastAPI**
- **Pydantic**
- **SQLite**
- **n8n**
- **Docker**
- **OpenRouter**
- **Mistral 7B**
- **Uvicorn**

## Repository structure

```text
ai-leads-crm/
├── data/
│   └── leads.db
├── n8n/
│   └── ai-leads-automation-workflow.json
├── python/
│   ├── app.py
│   ├── report.py
│   └── requirements.txt
└── README.md
```

## Engineering focus

This project explores several practical problems that appear when integrating LLMs into software systems:

- obtaining predictable structured outputs from generative models;
- validating model-generated data before it reaches application storage;
- separating workflow orchestration from backend responsibilities;
- handling type mismatches and malformed payloads between services;
- making AI decisions observable through persisted fields;
- connecting model outputs to deterministic business logic.

## Evaluation opportunities

A natural next step would be to add an evaluation layer for the AI component, including:

- classification accuracy by intent;
- priority-label consistency;
- score calibration;
- structured-output failure rate;
- comparison between models;
- prompt-version experiments;
- latency and cost tracking.

These extensions would turn the application into a useful testbed for studying reliability and evaluation of LLM-powered software systems.

## Running locally

Install the Python dependencies from `python/requirements.txt`, start the FastAPI application, and import the workflow from the `n8n/` directory into an n8n instance.

The database path can be configured with the `DB_PATH` environment variable.

## Author

**Pedro Marques Correa Domingues**  
B.Sc. Computer Science candidate  
Interests: AI systems, LLM evaluation, RAG, automation, and software engineering

[Portfolio](https://pedromcd.github.io) · [GitHub](https://github.com/pedromcd)
