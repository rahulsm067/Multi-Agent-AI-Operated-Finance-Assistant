# AI Tool Usage Log

This document tracks all AI tool usage, prompts, code generation steps, and model parameters used in the Multi-Agent Finance Assistant project.

---

## 1. LLMs & RAG
- **LLM Used:** [Specify model, e.g., OpenAI GPT-4, Llama-2, etc.]
- **Retriever:** FAISS (local), Pinecone (cloud)
- **Prompt Examples:**
  - "Summarize the risk exposure in Asia tech stocks for today."
  - "Highlight any earnings surprises in the Asia tech sector."
- **Parameters:**
  - `top_k`: 5
  - `temperature`: 0.2

## 2. Voice I/O
- **STT:** OpenAI Whisper
- **TTS:** Coqui TTS
- **Sample Prompts:**
  - "What's our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"

## 3. Data Ingestion
- **APIs:** yfinance, AlphaVantage
- **Scraping:** BeautifulSoup, requests
- **Document Loaders:** llama-index, unstructured

## 4. Orchestration
- **Frameworks:** FastAPI, LangGraph, CrewAI
- **Routing Logic:**
  - Voice input → STT → orchestrator → RAG/analysis → LLM → TTS or text
  - Fallback: If retrieval confidence < threshold, prompt user clarification via voice

---

## Code Generation Steps
- [Log each major code generation step, e.g., agent creation, pipeline setup, etc.]

---

## Model Parameters
- [Log all model parameters, hyperparameters, and configuration details.]

---

*Update this log as the project evolves and as new AI tools or models are integrated.* 