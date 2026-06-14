# Medical Chatbot App - Full Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Architecture Overview](#architecture-overview)
3. [Data Extraction Module](#data-extraction-module)
4. [Knowledge Graph Module](#knowledge-graph-module)
5. [Retriever Module](#retriever-module)
6. [Patient Memory & Report Analysis](#patient-memory--report-analysis)
7. [Installation & Setup](#installation--setup)

---

## Introduction
The **Medical Chatbot App** is a state-of-the-art hybrid Retrieval-Augmented Generation (RAG) and Knowledge-Augmented Generation (KAG) platform. It allows users to query complex medical topics using both unstructured text embeddings and structured knowledge graphs, while maintaining a robust memory of patient history and lab reports.

---

## Architecture Overview
The system is divided into three primary pipelines:
1. **Offline Data Ingestion**: Parses PDFs and text, generates embeddings, and saves them to `ChromaDB`.
2. **Knowledge Graph Processing**: Extracts explicit medical relationships (e.g., `Disease -> TREATED_WITH -> Medication`) using NLP (SciSpacy) and stores them as an accessible mathematical graph (NetworkX).
3. **Hybrid Retrieval Pipeline (KAG + RAG)**: Upon receiving a user query, it simultaneously retrieves semantic matches from the vector database and factual relationships from the graph, re-ranks the semantic matches using a Cross-Encoder, and synthesizes the final context into an LLM prompt.

---

## Data Extraction Module
Located in `Data_extraction/`. Responsible for translating raw medical text into dense vector embeddings.

### Core Scripts:
- **`document_loader.py`**: Interacts with the filesystem to load various unstructured documents (PDFs, text files). Converts raw files into standardized LangChain `Document` objects.
- **`text_splitter.py`**: Employs `RecursiveCharacterTextSplitter` to divide massive documents into optimal chunk sizes (typically 500-1000 tokens) with appropriate overlap. This ensures contexts fit within the LLM's context window.
- **`vector_store.py`**: The bridge to `ChromaDB`. It instantiates the embedding model (e.g., HuggingFace embeddings or OpenAI) and provides methods to `add_documents` or perform similarity searches.
- **`ingestion.py`**: The entrypoint script. Runs the entire pipeline sequentially: Load -> Split -> Embed -> Store.

---

## Knowledge Graph Module
Located in `knowledge_graph/`. Extracts exact medical facts to ground the LLM responses and prevent clinical hallucinations.

### Core Scripts:
- **`entity_extractor.py`**: Uses `scispacy` (e.g., `en_core_sci_sm` model) to perform Named Entity Recognition (NER). It identifies specific medical entities (Symptoms, Drugs, Diseases) and infers relationships based on linguistic patterns.
- **`graph_builder.py`**: Takes the extracted triples (Subject, Predicate, Object) and uses `NetworkX` to construct a directed graph. Nodes represent entities; edges represent the relationship types.
- **`graph_retriever.py`**: Provides the `GraphRetriever` class. Given a natural language query, it extracts the key entities from the query, searches the graph for the matching nodes, and extracts the 1-hop or 2-hop neighborhood to provide exact factual context.

---

## Retriever Module
Located in `retriever/`. This is the execution engine of the chatbot.

### Core Scripts:
- **`kag_rag_pipeline.py`**: Defines the `KAGRAGPipeline` class. 
  - *Methods*: `generate_response()`
  - *Logic*: Calls the Graph Retriever and Vector Retriever in parallel. Merges both contexts into a single meta-prompt and queries the LLM.
- **`retrieve.py`**: Defines the `MedicalRetriever` class. Interfaces with `ChromaDB` to fetch semantically relevant chunks. Uses Maximum Marginal Relevance (MMR) or standard Similarity Search.
- **`reranker.py`**: Defines `BGEReranker` (or `MedicalReranker`). Uses a Cross-Encoder (`BAAI/bge-reranker-base`) to score the retrieved document chunks against the user query. Documents with low relevancy are filtered out, drastically improving RAG precision.
- **`llm.py`**: Standardizes the initialization of Language Models (OpenAI, Groq) to be injected into the various pipelines.
- **`prompt.py`**: Contains the `SYSTEM_PROMPT` and other critical prompt templates that instruct the LLM on how to behave like a compassionate, highly technical clinical assistant.
- **`config.py`**: Exposes configuration constants like `CHROMA_PATH` and `EMBEDDING_MODEL`.

---

## Patient Memory & Report Analysis
Integrated within the retriever but heavily focused on specific patient workflows.

- **`memory.py`**: Uses Python's `sqlite3` to maintain persistent databases (`clinic_test.db`, `temp_db`). Features include:
  - `upsert_patient_profile()`: Saves demographics, conditions, and allergies.
  - `add_message()` / `get_chat_history()`: Tracks the conversation history natively so the bot remembers past turns.
- **`report_analyzer.py`**: The OCR and structured output layer.
  - Can natively read PDF metadata via `pypdf`.
  - Automatically falls back to `pytesseract` and `pdf2image` to perform Optical Character Recognition on faxes or scanned documents.
  - Utilizes LangChain's `.with_structured_output()` to force the LLM to output a strict JSON schema containing: `patient_name`, `report_date`, `extracted_entities`, and a `patient_explanation`.

---

## Installation & Setup

### Prerequisites
1. **Python 3.9+** is required.
2. Ensure you have **Tesseract OCR** and **Poppler** installed on your OS for the OCR features.

### Python Dependencies
```bash
# Core AI and Retrieval
pip install langchain langchain-openai langchain-groq sentence-transformers chromadb

# Knowledge Graph
pip install networkx spacy scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_core_sci_sm-0.5.4.tar.gz

# Document Processing
pip install pypdf pytesseract pdf2image
```

### Environment Variables
Create a `.env` in the root directory:
```env
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
```

### Running the App
1. **Build the Database**: Run `python Data_extraction/ingestion.py` to embed your local files.
2. **Analyze a Lab Report**: Run `python retriever/report_analyzer.py` to OCR a PDF and save it to the SQLite patient memory.
3. **Query the Graph**: Run `python knowledge_graph/graph_retriever.py` to test relationship extraction.
4. **Chat Interface**: Import and instantiate `KAGRAGPipeline` from `kag_rag_pipeline.py` to begin passing user queries.
