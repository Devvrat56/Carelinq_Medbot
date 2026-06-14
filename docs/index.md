# Medical Chatbot App Documentation

Welcome to the documentation for the Medical Chatbot App. This project implements a comprehensive Retrieval-Augmented Generation (RAG) and Knowledge-Augmented Generation (KAG) system tailored for the medical domain.

## Overview

The Chatbot is designed to accurately answer complex clinical queries, analyze patient lab reports, and manage medical knowledge effectively. The system is modularized into three core components:

1. **[Data Extraction](data_extraction.md)**: Handling document ingestion, chunking, parsing, and persisting the embedded vectors into a vector database (e.g., ChromaDB).
2. **[Knowledge Graph](knowledge_graph.md)**: Medical entity extraction (using models like SciSpacy) and graph building/retrieval (using NetworkX).
3. **[Retriever & RAG Pipeline](retriever.md)**: The core engine that retrieves contexts, reranks them, interacts with the Knowledge Graph, generates prompt context, and interfaces with LLMs to provide final answers. It also handles patient memory and PDF report analysis.

## Core Databases

- **chroma_db**: Persistent vector store for document embeddings.
- **temp_db**: Temporary or cache databases (e.g., SQLite for chat histories).
- **clinic_test.db**: SQLite database used by the Memory module for patient profiles.

## Setup & Configuration

- Use `.env` to store your sensitive keys (`OPENAI_API_KEY`, `GROQ_API_KEY`).
- Standard dependencies include `langchain`, `pypdf`, `pytesseract`, `networkx`, `scispacy`, and `spacy`.
