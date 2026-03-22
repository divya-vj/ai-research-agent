---
title: AI Research Assistant Agent
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: docker
sdk_version: "1.0"
app_file: app.py
pinned: false
---

# 🔬 AI Research Assistant Agent

An autonomous AI agent that researches any topic by searching the web,
synthesising information from multiple sources, and producing a structured
research report with citations — in under 60 seconds.

**[Live Demo](https://huggingface.co/spaces/Divyavj1/research-assistant-agent)**

---

## What Problem This Solves

Research takes hours. Finding sources, reading articles, taking notes,
identifying patterns — this agent does all of that in 60 seconds autonomously.

---

## How the Agent Works

The agent uses the ReAct framework — Reasoning and Acting:

1. Receives research topic from user
2. Plans what to search for
3. Searches web using Tavily API (3-5 searches)
4. Analyses each result
5. Decides if more information is needed
6. Synthesises all findings into structured report
7. User downloads as PDF or text

---

## Tech Stack

| Technology | Purpose |
|---|---|
| LangChain Agents | ReAct agent framework |
| Tavily API | AI-optimised web search |
| Groq Llama-3.1 | LLM reasoning and synthesis |
| FPDF2 | PDF report generation |
| Streamlit | Web interface |
| Hugging Face Spaces | Deployment |

---

## Run Locally

git clone https://github.com/divya-vj/ai-research-agent.git
cd ai-research-agent
pip install -r requirements.txt

Add GROQ_API_KEY and TAVILY_API_KEY to .env file

streamlit run app.py

Get free API keys at:
- Groq: console.groq.com
- Tavily: tavily.com

---

