# Medbot Data Ingestion Pipeline

This module is responsible for loading medical documents, chunking the text into manageable pieces, generating embeddings, and storing them in a local Chroma vector database for Retrieval-Augmented Generation (RAG).

## Features

- **Document Loading:** Supports custom JSON format with pre-extracted text, as well as raw PDFs, Text files, and CSVs.
- **Text Splitting:** Uses LangChain's `RecursiveCharacterTextSplitter` to semantically chunk large documents to fit within the context limits of the embedding models.
- **Vector Storage:** Automatically converts chunks into vector embeddings using HuggingFace's `sentence-transformers/all-MiniLM-L6-v2` model and stores them in ChromaDB.

## Structure

- `document_loader.py`: Contains the `DocumentLoader` class that reads files from a given directory and converts them into LangChain `Document` objects. It seamlessly handles custom `.json` extractions to preserve metadata like the source filename.
- `text_splitter.py`: Contains the `DocumentSplitter` class to configure and execute text chunking.
- `vector_store.py`: Contains the `VectorStoreManager` to handle embedding initialization and storage into the local Chroma database.
- `ingestion.py`: The main orchestrator script that ties the components together into an automated pipeline.

## Prerequisites

Ensure you have the required Python packages installed. You can install them via pip:

```bash
pip3 install langchain langchain-community langchain-core pypdf sentence-transformers chromadb unstructured langchain-huggingface
```

## How to Run

To run the data ingestion pipeline, use the `ingestion.py` script from the root directory of the project.

### Basic Usage

To ingest the default JSON files located in `./Data_extraction/json`:

```bash
python3 -m Data_extraction.ingestion --data_dir "./Data_extraction/json" --persist_dir "./chroma_db"
```

### Configuration Options

You can configure the pipeline by passing additional command-line arguments:

- `--data_dir`: The directory containing your medical documents or JSONs (default: `./data`).
- `--persist_dir`: The directory where the Chroma vector database will be saved (default: `./chroma_db`).
- `--chunk_size`: The maximum character length of each chunk (default: `1000`).
- `--chunk_overlap`: The character overlap between consecutive chunks to maintain context (default: `200`).
- `--embedding_model`: The HuggingFace embedding model to use (default: `sentence-transformers/all-MiniLM-L6-v2`).

**Example with custom chunking:**
```bash
python3 -m Data_extraction.ingestion --data_dir "./Data_extraction/json" --chunk_size 1500 --chunk_overlap 300
```

## Output

Upon successful execution, a directory (e.g., `./chroma_db`) will be created in your specified location. This directory contains the SQLite database and vector indices required by ChromaDB to perform fast semantic similarity searches during the chatbot's retrieval phase.
