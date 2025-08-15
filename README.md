# 🩺 GesundLotse – AI-Powered Clinical Chat Assistant

**GesundLotse** is an empathetic, evidence-based medical guidance assistant that simulates a real doctor’s consultation style.  
It combines **retrieval-augmented generation (RAG)**, **PubMed (NCBI)** data lookup, and **web search** to provide safe, structured, and context-aware health advice.

⚠ **Disclaimer:** This tool does **not** replace professional medical care. For emergencies, always call your local emergency number.

---

## ✨ Features

- **Doctor-style Interview Flow** – Starts with 1–4 adaptive, clinically relevant questions before giving advice.
- **Evidence-Driven Guidance** – Uses PubMed (via NCBI API) and trusted clinical guidelines.
- **RAG Pipeline** – Retrieves relevant context from your indexed medical documents stored in Pinecone.
- **Web Search Integration** – Fetches recent and relevant public health information using the Serper API.
- **Multilingual Support** – Automatically detects German or English and responds accordingly.
- **Session Memory** – Remembers conversation history for contextual follow-ups.
- **Beautiful Web UI** – Clean, responsive chat interface with an empathetic intro card.

---

## 🏗 Architecture
