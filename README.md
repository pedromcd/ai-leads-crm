# AI Leads CRM – Sistema Inteligente de Qualificação de Leads

🇧🇷 Versão em Português abaixo  
🇺🇸 English version below

---

# 🇧🇷 Versão em Português

## 📌 Visão Geral

O **AI Leads CRM** é um sistema completo de qualificação automática de leads utilizando Inteligência Artificial, automação de workflows e backend customizado.

O sistema recebe leads via webhook, utiliza um modelo de linguagem (LLM) para classificar intenção, definir prioridade e score, gerar resposta sugerida e armazenar os dados estruturados em um banco SQLite.

Este projeto simula uma aplicação real de IA aplicada ao negócio, com arquitetura modular e separação clara entre automação e backend.

---

## 🚀 Arquitetura

Webhook (n8n)  
→ Classificação com LLM (OpenRouter – Mistral 7B)  
→ Parsing e normalização do JSON  
→ Backend FastAPI  
→ Banco de dados SQLite  

---

## 🧠 Funcionalidades

- Recebimento automático de leads via webhook
- Classificação de intenção (Pricing, Trial, Support, etc.)
- Definição automática de prioridade (Low, Medium, High, Urgent)
- Score inteligente de 0 a 100
- Geração de resposta sugerida para atendimento
- Persistência dos dados em banco SQLite
- API REST desenvolvida com FastAPI
- Orquestração do fluxo com n8n

---

## 🛠 Tecnologias Utilizadas

- Python
- FastAPI
- SQLite
- n8n (Docker)
- OpenRouter (API de LLM)
- Uvicorn

---

## 📂 Estrutura do Projeto

ai-leads-crm/
│
├── python/
│   ├── app.py
│   ├── report.py
│   └── requirements.txt
│
├── data/
│   └── leads.db
│
├── n8n/
│   └── ai-leads-automation-workflow.json
│
└── README.md

---

## 📊 Relatórios

O projeto inclui um script simples para análise dos dados armazenados.

Execute:

python report.py

O relatório exibe:
- Total de leads
- Leads por intenção
- Leads por prioridade
- Média de score

---

## 🎯 Caso de Uso

Este sistema pode ser aplicado em:

- EdTechs
- Empresas SaaS
- Times de vendas
- Automação de marketing
- Qualificação automática de inbound leads

---

## 📚 Principais Aprendizados

- Orquestração de LLMs em fluxos automatizados
- Extração estruturada de JSON a partir de respostas de IA
- Validação e persistência backend
- Separação clara entre camada de automação e API
- Construção de arquitetura modular para aplicações de IA

---

# 🇺🇸 English Version

## 📌 Overview

**AI Leads CRM** is an end-to-end automated lead qualification system built using workflow automation and Large Language Models (LLMs).

The system receives inbound leads via webhook, uses an LLM to classify intent, assign priority and score, generate a suggested reply, and store structured data in a SQLite database.

This project simulates a real-world AI-powered business application with clean architecture and modular separation between automation and backend.

---

## 🚀 Architecture

Webhook (n8n)  
→ LLM Classification (OpenRouter – Mistral 7B)  
→ JSON Parsing & Normalization  
→ FastAPI Backend  
→ SQLite Database  

---

## 🧠 Features

- Automatic lead intake via webhook
- AI-powered intent classification
- Automatic priority detection
- Intelligent scoring system (0–100)
- Suggested reply generation
- Persistent storage using SQLite
- REST API built with FastAPI
- Workflow orchestration using n8n

---

## 🛠 Tech Stack

- Python
- FastAPI
- SQLite
- n8n (Docker)
- OpenRouter (LLM API)
- Uvicorn

---

## 📊 Reporting

The project includes a simple reporting script.

Run:

python report.py

It outputs:
- Total leads
- Leads by intent
- Leads by priority
- Average score

---

## 🎯 Use Case

This system can be applied to:

- EdTech companies
- SaaS platforms
- Sales automation
- Marketing automation pipelines
- Intelligent inbound lead qualification

---

## 📚 Key Learnings

- LLM orchestration in automation workflows
- Structured JSON extraction from AI outputs
- Backend validation and persistence
- Modular AI application architecture

---

## 👨‍💻 Author

Pedro Marques  
Computer Science Undergraduate  
Automation & AI Enthusiast