# Retriever Module

The `retriever` module acts as the brain of the chatbot. It coordinates document retrieval, graph retrieval, prompt assembly, and interactions with the Language Models.

## Core RAG & KAG Components

- **`kag_rag_pipeline.py`**: The ultimate orchestration layer. It combines standard RAG contexts with Knowledge Graph contexts and sends a unified prompt to the LLM via `generate_response`.
- **`rag_pipeline.py`**: A standard LangChain-based Retrieval-Augmented Generation pipeline.
- **`retrieve.py`**: Contains the core logic for searching the vector store and pulling the top-K relevant document chunks.
- **`reranker.py`**: Implements re-ranking (often via cross-encoders or specialized scoring) to reorder the retrieved documents so the most highly relevant chunks appear first.

## Auxiliary Components

- **`llm.py`**: A wrapper or manager for initializing the Language Models (e.g., OpenAI or Groq).
- **`prompt.py`**: Central repository for all system prompts, chain-of-thought instructions, and QA templates used by the models.
- **`config.py`**: Centralized configuration variables for the retriever module.

## Patient Context & Analysis

- **`report_analyzer.py`**: Parses patient medical PDFs (using native text and OCR via `pytesseract` / `pdf2image`) to extract lab results and provide plain-English summaries.
- **`memory.py`**: Manages session state and patient profiles using an SQLite database. It saves patient histories, allergies, and the conversational history of the chatbot so that subsequent queries are contextually aware.
