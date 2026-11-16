[English](README.md) | **Português**

# 🤖 AI Leads CRM

**Pipeline automatizado de qualificação de leads: um workflow no n8n envia cada lead recebido para um LLM via OpenRouter, transforma a resposta em dados estruturados, e um backend em FastAPI valida e salva tudo em SQLite.**

O objetivo é mostrar como um modelo de linguagem se encaixa em um **fluxo de negócio real**: não como um chatbot isolado, e sim como uma etapa de um pipeline com orquestração, validação, persistência e relatório.

---

## 🎯 Problema e objetivo

Pequenas empresas recebem leads por formulário, WhatsApp e redes sociais, e alguém precisa ler cada mensagem para decidir: *o que essa pessoa quer? Qual a urgência? O que devemos responder?* Essa triagem é repetitiva e fácil de atrasar.

Este projeto automatiza a primeira triagem:

1. o lead chega por um **webhook**;
2. um **LLM** classifica a intenção, define a prioridade e uma pontuação de 0 a 100, sugere a próxima ação e escreve um rascunho de resposta;
3. o resultado é **validado** e **armazenado**, para que a equipe atenda primeiro os leads mais quentes e analise o funil depois.

---

## ⚙️ Como funciona

```text
POST /webhook/lead  (name, email, phone, source, message)
        │
        ▼
┌────────────────────────── workflow n8n ───────────────────────────┐
│ 1. Webhook          recebe o lead                                 │
│ 2. Edit Fields      normaliza os campos de entrada                │
│ 3. OpenRouter       chama o mistralai/mistral-7b-instruct         │
│                     (o prompt de sistema exige apenas JSON)       │
│ 4. Code (JS)        remove cercas de Markdown, faz o parse,       │
│                     usa valores padrão seguros se o parse falhar  │
│                     e junta os campos da IA com os dados do lead  │
│ 5. HTTP Request     POST para o backend em FastAPI                │
│ 6. Respond          {"ok": true, "lead_saved": true}              │
└───────────────────────────────────────────────────────────────────┘
        │
        ▼
FastAPI  POST /lead  → validação Pydantic → score limitado a 0–100 → SQLite
        │
        ▼
GET /leads (leads mais recentes)   ·   report.py (totais por intenção e prioridade, score médio)
```

### O que o modelo retorna

O prompt de sistema restringe a saída a um esquema fixo, com conjuntos fechados de rótulos:

| Campo | Valores permitidos |
|---|---|
| `intent` | `Pricing`, `Trial`, `Support`, `General`, `Partnership` |
| `priority` | `Low`, `Medium`, `High`, `Urgent` |
| `score` | inteiro de 0 a 100 |
| `next_action` | texto curto |
| `suggested_reply` | resposta curta em português, no estilo WhatsApp |

Exemplo ilustrativo de lead armazenado:

```json
{
  "id": "3f9a1c2e",
  "created_at": "2026-09-25T14:32:10",
  "name": "Ana",
  "source": "instagram",
  "message": "Oi! Quanto custa o plano anual para 5 usuários?",
  "intent": "Pricing",
  "priority": "High",
  "score": 82,
  "next_action": "Enviar a tabela de preços do plano anual",
  "suggested_reply": "Oi, Ana! Te envio agora os valores do plano anual para 5 usuários 😊",
  "status": "NEW"
}
```

---

## 🧱 Decisões de engenharia

- **Orquestração separada do backend.** O n8n cuida do fluxo (receber o lead, chamar o modelo, encaminhar o resultado); o FastAPI cuida apenas de validação e persistência. Cada parte pode mudar sem quebrar a outra.
- **Nunca confiar cegamente na saída do modelo.** LLMs às vezes envolvem o JSON em Markdown ou devolvem JSON inválido. O nó Code limpa a resposta e, se o parse ainda falhar, usa valores neutros (`General`, `Medium`, `50`) para que o lead nunca se perca.
- **Segunda camada de validação na API.** O Pydantic rejeita payloads com campos faltando ou de tipo errado, e o score é limitado a 0–100 antes de ser gravado.
- **Rótulos fechados.** Restringir `intent` e `priority` a valores fixos torna os dados agregáveis (relatórios, dashboards), em vez de texto livre.
- **Temperatura baixa (0.3)** para classificações mais consistentes.

---

## 🛠️ Tecnologias

- **n8n** (Docker): orquestração do workflow
- **OpenRouter** + **Mistral 7B Instruct**: classificação com LLM
- **Python**, **FastAPI**, **Pydantic**, **Uvicorn**: API e validação
- **SQLite**: armazenamento
- **JavaScript**: tratamento da resposta dentro do n8n

---

## 🔌 API

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/health` | Health check; também retorna o caminho do banco |
| `POST` | `/lead` | Valida e armazena um lead analisado; retorna o `lead_id` |
| `GET` | `/leads?limit=50` | Lista os leads mais recentes |

A documentação interativa fica em `http://localhost:8000/docs` (Swagger UI do FastAPI).

---

## ▶️ Como executar localmente

### 1. Backend

```bash
git clone https://github.com/pedromcd/ai-leads-crm.git
cd ai-leads-crm/python
pip install fastapi uvicorn pydantic
uvicorn app:app --reload --port 8000
```

O banco é criado automaticamente em `../data/leads.db`. Para usar outro local, defina a variável de ambiente `DB_PATH`.

### 2. n8n

```bash
cd ../n8n
docker compose up -d
```

Abra `http://localhost:5678` (o compose ativa autenticação básica com credenciais de desenvolvimento local; troque-as antes de expor o n8n em qualquer lugar).

### 3. Importar o workflow

1. No n8n, importe `n8n/n8n-ai-leads-crm-workflow.json`.
2. No nó **OpenRouter**, defina o header `Authorization` como `Bearer <sua chave da OpenRouter>`. Nenhuma chave fica armazenada neste repositório.
3. Ative o workflow. O nó **HTTP Request** já aponta para `http://host.docker.internal:8000/lead`, o backend rodando na sua máquina.

### 4. Enviar um lead de teste

```bash
curl -X POST http://localhost:5678/webhook/lead \
  -H "Content-Type: application/json" \
  -d '{"name":"Ana","email":"ana@example.com","source":"instagram","message":"Quanto custa o plano anual para 5 usuários?"}'
```

Depois confira o resultado:

```bash
curl http://localhost:8000/leads
cd python && python report.py
```

---

## 🧩 Estrutura

```text
ai-leads-crm/
├── n8n/
│   ├── docker-compose.yml                  # Instância local do n8n
│   └── n8n-ai-leads-crm-workflow.json      # Workflow exportado (sem credenciais)
├── python/
│   ├── app.py                              # FastAPI: /health, /lead, /leads
│   └── report.py                           # Totais por intenção/prioridade e score médio
└── data/                                   # Banco SQLite (criado em tempo de execução)
```

---

## 🚧 Próximos passos

- **Avaliar o classificador:** montar um pequeno conjunto de leads rotulados e medir a acurácia da intenção, a consistência da prioridade e a taxa de JSON malformado, comparando modelos e versões de prompt.
- Usar o modo de **saída estruturada / JSON schema** da OpenRouter, em vez de depender só do prompt.
- Adicionar `requirements.txt`, Docker para o backend e testes automatizados.
- Criar um endpoint para atualizar o `status` do lead (NEW → CONTACTED → WON/LOST) e um dashboard simples.

---

## 👨‍💻 Autor

**Pedro Marques Correa Domingues** · [GitHub](https://github.com/pedromcd) · [Portfólio](https://pedromcd.github.io)
