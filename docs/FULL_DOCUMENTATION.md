# Carelinq MedBot - Technical Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Orchestration Layer (`main.py`)](#orchestration-layer)
3. [Frontend Interface (`frontend/`)](#frontend-interface)
4. [Data Extraction Module (`Data_extraction/`)](#data-extraction-module)
5. [Knowledge Graph Module (`knowledge_graph/`)](#knowledge-graph-module)
6. [Data Safety & Metrics (`Data_safety/`)](#data-safety--metrics)
7. [Retriever & Memory (`retriever/`)](#retriever--memory)
8. [Evaluation Framework (`evaluation/`)](#evaluation-framework)

---

## Architecture Overview
The Carelinq MedBot is a production-grade, hybrid RAG (Retrieval-Augmented Generation) and KAG (Knowledge-Augmented Generation) clinical consultation platform. It seamlessly ingests unstructured clinical guidelines and multimodal patient reports, mapping them to a persistent mathematical Knowledge Graph, and surfaces answers dynamically using rigorous safety and hallucination heuristics.

---

## Orchestration Layer

### `main.py`
The master orchestrator defining the entry point for the application. It features a Dual-Interface architecture:
- **FastAPI Backend (`uvicorn main:app`)**: Exposes REST endpoints (`/chat`, `/upload-report`, `/patient/{id}`) for production environments. Features CORS middleware to securely serve decoupled clients.
- **Interactive CLI (`python main.py`)**: A developer terminal interface designed for offline testing and debugging without needing to launch a web server.

---

## Frontend Interface

### `frontend/streamlit_app.py`
A completely decoupled React-based client (via Streamlit) that hooks into the FastAPI backend.
- **State Management**: Real-time synchronization of `patient_id` state against the SQLite backend to instantly populate historical `chat_history`.
- **Multimodal Ingestion**: A drag-and-drop sidebar widget that posts PDFs/Images directly to the OCR/Extraction pipeline endpoint.
- **Metric Formatting**: Natively parses the backend JSON to elegantly display *Confidence Scores*, *Safety Checkmarks*, and *Grounded Footnotes*.

---

## Data Extraction Module
Located in `Data_extraction/`. Handles bulk ingestion of clinical guidelines.

### Core Scripts:
- **`document_loader.py`**: Interacts with the filesystem to load unstructured documents and converts them to LangChain `Document` objects.
- **`text_splitter.py`**: Optimizes chunk configurations for the `all-MiniLM-L6-v2` embedding limits using `RecursiveCharacterTextSplitter`.
- **`vector_store.py`**: Manages the local `ChromaDB` instance (`chroma_db`).
- **`ingestion.py`**: The offline batch pipeline script: Load -> Split -> Embed -> Store.

---

## Knowledge Graph Module
Located in `knowledge_graph/`. Enforces deterministic factual accuracy by mapping clinical documents to strict network graphs.

### Core Scripts:
- **`entity_extractor.py`**: Utilizes `scispacy` (`en_core_sci_sm`) to perform NER, extracting explicit subject-predicate-object triples.
- **`graph_builder.py`**: Translates triples into a persistent `NetworkX` directed graph object.
- **`graph_retriever.py`**: Executes 1-hop and 2-hop neighborhood searches based on entities isolated from the user's live query.
- **`kg_updater.py`**: A dynamic pipeline that automatically injects new structured entities (extracted from uploaded patient reports) back into the active Knowledge Graph.

---

## Data Safety & Metrics
Located in `Data_safety/`. The heuristic layer enforcing clinical rigor.

### Core Scripts:
- **`confidence.py`**: Blends traditional `Chroma` retriever distance metrics with the logits emitted from the `bge-reranker-base` cross-encoder to calculate a global percentage confidence score.
- **`hallucination_checker.py`**: A lightweight lexical overlap engine verifying that the LLM's final generated answer is strictly grounded in the retrieved context chunks.
- **`safety.py`**: An upfront sanitization filter rejecting out-of-bounds, non-medical, or high-risk queries.

---

## Retriever & Memory
Located in `retriever/`. The execution engine handling memory and LLM querying.

### Core Scripts:
- **`kag_rag_pipeline.py`**: The central aggregation logic. Parallelizes KAG and RAG fetching, injects patient memory, and packages the result for `main.py`.
- **`retrieve.py` / `reranker.py`**: The core RAG mechanics (Vector Search + Cross-Encoder Reranking).
- **`memory.py`**: Exposes the `PatientMemoryManager`. It defines a robust SQLite schema managing the `patients` table, `reports` tracking, and sequential `chat_history`.
- **`report_analyzer.py`**: Features multi-modal fallbacks (`pypdf` -> `pytesseract` OCR). It uses `Langchain`'s `.with_structured_output()` and strict Pydantic schemas to ensure parsed reports map precisely to clinical structures (e.g. Prostate & Breast Cancer matrices).
- **`citation_manager.py`**: Maps generated text spans back to their source document URIs.

---

## Evaluation Framework
Located in `evaluation/`. The framework for automated CI/CD metric validation.

### Core Scripts:
- **`ragas_eval.py`**: Integrates the RAGAS framework to run automated tests measuring *Faithfulness* (Are facts invented?) and *Answer Relevance* (Does it answer the prompt directly?).
- **`test_queries.json`**: Standardized benchmarking dataset.
