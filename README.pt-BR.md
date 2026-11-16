[English](README.md) | **Português**

# AI Leads CRM

**Pipeline de qualificação de leads com LLM, usando n8n, FastAPI, OpenRouter e SQLite.**

Este projeto mostra como um modelo de linguagem pode ser integrado a um fluxo de negócio de ponta a ponta, em vez de ser usado como um chatbot isolado. Os leads recebidos são processados por um pipeline automatizado, convertidos em saídas estruturadas pela IA, validados por uma API de backend e persistidos para análise posterior.

## Fluxo do sistema

```text
Lead recebido
    ↓
Webhook do n8n
    ↓
Classificação por LLM via OpenRouter
    ↓
Saída estruturada em JSON
    ↓
Validação no FastAPI
    ↓
Persistência no SQLite
    ↓
Relatórios / ações posteriores
```

A etapa de IA produz campos estruturados como:

```json
{
  "intent": "...",
  "priority": "...",
  "score": 0,
  "next_action": "...",
  "suggested_reply": "..."
}
```

## O que o sistema faz

- recebe leads por um webhook do n8n;
- classifica a intenção do lead com um LLM;
- atribui prioridade;
- gera uma pontuação de 0 a 100;
- sugere a próxima ação;
- gera uma sugestão de resposta;
- valida o payload estruturado com Pydantic/FastAPI;
- persiste o resultado no SQLite;
- expõe endpoints de API para consultar os leads armazenados;
- oferece um script de relatório para análises básicas.

## Modelo do backend

O backend em FastAPI valida o payload do lead antes de armazená-lo:

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

A pontuação é normalizada para o intervalo aceito de 0 a 100 antes da persistência.

## API

### Health check

```http
GET /health
```

### Armazenar um lead analisado

```http
POST /lead
```

### Listar leads recentes

```http
GET /leads
```

## Stack

- **Python**
- **FastAPI**
- **Pydantic**
- **SQLite**
- **n8n**
- **Docker**
- **OpenRouter**
- **Mistral 7B**
- **Uvicorn**

## Estrutura do repositório

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

## Foco de engenharia

Este projeto explora vários problemas práticos que surgem ao integrar LLMs em sistemas de software:

- obter saídas estruturadas previsíveis de modelos generativos;
- validar os dados gerados pelo modelo antes que cheguem ao armazenamento da aplicação;
- separar a orquestração do fluxo das responsabilidades do backend;
- lidar com tipos incompatíveis e payloads malformados entre serviços;
- tornar as decisões da IA observáveis por meio de campos persistidos;
- conectar as saídas do modelo a regras de negócio determinísticas.

## Oportunidades de avaliação

Um próximo passo natural seria adicionar uma camada de avaliação para o componente de IA, incluindo:

- acurácia da classificação por intenção;
- consistência dos rótulos de prioridade;
- calibração da pontuação;
- taxa de falha da saída estruturada;
- comparação entre modelos;
- experimentos com versões de prompt;
- acompanhamento de latência e custo.

Essas extensões transformariam a aplicação em um ambiente de testes útil para estudar a confiabilidade e a avaliação de sistemas de software baseados em LLMs.

## Executando localmente

Instale as dependências Python de `python/requirements.txt`, inicie a aplicação FastAPI e importe o workflow do diretório `n8n/` em uma instância do n8n.

O caminho do banco de dados pode ser configurado pela variável de ambiente `DB_PATH`.

## Autor

**Pedro Marques Correa Domingues**  
Graduando em Ciência da Computação  
Interesses: sistemas de IA, avaliação de LLMs, RAG, automação e engenharia de software

[Portfólio](https://pedromcd.github.io) · [GitHub](https://github.com/pedromcd)
