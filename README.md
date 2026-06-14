<h1 align="center">Carelinq MedBot</h1>

<p align="center">
  <strong>A Production-Grade Medical Consultation Chatbot powered by Hybrid KAG + RAG Architecture.</strong>
</p>

## Overview

The Carelinq MedBot is an advanced clinical assistant designed to analyze patient reports, query rigorous medical guidelines, and provide highly grounded responses. It combines the deterministic accuracy of a **Knowledge Graph (KAG)** with the semantic flexibility of a **Vector Database (RAG)**, wrapped entirely in a robust Safety and Memory orchestration layer.

### Key Features
- 🛡️ **Safety & Metrics**: Built-in Confidence Scoring, Lexical Hallucination Checking, and query sanitization.
- 🧠 **Persistent Patient Memory**: SQLite-backed patient tracking holding comprehensive histories, clinical profiles, and prior chat turns.
- 📄 **Multimodal Report Ingestion**: Upload a PDF or Image (with Tesseract OCR fallback), extract data strictly using Pydantic Schemas, and auto-populate the Knowledge Graph.
- 🚀 **Dual Interface**: Fully decoupled `FastAPI` REST backend and a beautiful interactive `Streamlit` frontend.

---

## 🛠️ Installation & Setup

1. **Prerequisites**: Ensure you have Python 3.9+ and system-level `tesseract-ocr` installed.
2. **Install Dependencies**:
```bash
pip install -r requirements.txt
```
*(Note: Ensure you download the `en_core_sci_sm` scispacy model if it doesn't auto-resolve.)*

3. **Configure Environment**: Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_actual_api_key_here
```

---

## 🚀 Running the Application

Because this application utilizes a modern, decoupled architecture, you will need two terminal windows.

**1. Launch the Backend API (Terminal 1)**
```bash
uvicorn main:app --reload
```
*Your FastAPI backend is now serving endpoints at `http://localhost:8000`.*

**2. Launch the Streamlit Frontend (Terminal 2)**
```bash
streamlit run frontend/streamlit_app.py
```
*Your browser will automatically open the interactive clinical interface!*

---

## 📚 Project Architecture

For a deep dive into the technical capabilities of each module, please read the [FULL_DOCUMENTATION.md](docs/FULL_DOCUMENTATION.md).

- `/Data_extraction/` - Unstructured document loading and offline embedding pipelines.
- `/Data_safety/` - Confidence scoring and hallucination heuristics.
- `/docs/` - Technical documentation.
- `/evaluation/` - Automated RAGAS testing frameworks.
- `/frontend/` - Streamlit User Interface.
- `/knowledge_graph/` - SciSpacy NER and NetworkX graph generation.
- `/retriever/` - The orchestration logic handling LLMs, Cross-Encoders, structured output Pydantic parsers, and persistent SQLite memory.
