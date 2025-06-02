# Multi-Agent Finance Assistant

## Overview
A modular, multi-source, multi-agent finance assistant that delivers spoken market briefs via a Streamlit app. The system leverages advanced data-ingestion pipelines, vector store indexing for Retrieval-Augmented Generation (RAG), and orchestrates specialized agents (API, scraping, retrieval, analytics, LLM, voice) via FastAPI microservices. Voice I/O is powered by open-source toolkits, and text agents are built with LangGraph and CrewAI. All code is open-source, documented with AI-tool usage logs, and deployed on Streamlit.

-



### Agent Roles
- **API Agent:** Polls real-time & historical market data via AlphaVantage or Yahoo Finance
- **Scraping Agent:** Crawls filings using Python loaders
- **Retriever Agent:** Indexes embeddings in FAISS or Pinecone and retrieves top-k chunks
- **Analysis Agent:** Computes risk exposure, allocation changes, and quantitative summaries
- **Language Agent:** Synthesizes narrative via LLM using LangChain's retriever interface
- **Voice Agent:** Handles STT (Whisper) → LLM → TTS pipelines

### Orchestration & Communication
- Microservices built with FastAPI for each agent
- Routing logic: voice input → STT → orchestrator → RAG/analysis → LLM → TTS or text
- Fallback: if retrieval confidence < threshold, prompt user clarification via voice

---

## Use Case: Morning Market Brief
Every trading day at 8 AM, a portfolio manager asks:
> "What's our risk exposure in Asia tech stocks today, and highlight any earnings surprises?"

The system responds verbally:
> "Today, your Asia tech allocation is 22% of AUM, up from 18% yesterday. TSMC beat estimates by 4%, Samsung missed by 2%. Regional sentiment is neutral with a cautionary tilt due to rising yields."

---

## Directory Structure
```
/agents/                # All agent microservices (API, Scraper, Retriever, Analysis, Language, Voice)
/data_ingestion/        # Data loaders, API wrappers, scrapers
/orchestrator/          # FastAPI orchestrator for routing and agent coordination
/streamlit_app/         # Streamlit UI for user interaction
/docs/                  # Documentation, AI tool usage logs, architecture diagrams
/tests/                 # Unit and integration tests
requirements.txt        # Python dependencies
Dockerfile              # For containerization
README.md               # Setup, architecture, benchmarks, etc.
```

---

## Setup & Deployment
1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd Multi-Agent-Finance-Assistant
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run agents and orchestrator:**
   ```bash
   # Example (update as needed)
   python agents/api_agent.py
   python agents/scraping_agent.py
   python orchestrator/coordinator.py
   # ...
   ```
4. **Start Streamlit app:**
   ```bash
   streamlit run streamlit_app/app.py
   ```
5. **(Optional) Docker deployment:**
   ```bash
   docker build -t finance-assistant .
   docker run -p 8501:8501 finance-assistant
   ```

---

## AI Tool Usage & Benchmarks
- See `docs/ai_tool_usage.md` for detailed logs of AI tool prompts, code generation steps, and model parameters.
- Performance benchmarks and framework/toolkit comparisons are also documented in the `docs/` folder.

---

## License
Open-source, MIT License.
