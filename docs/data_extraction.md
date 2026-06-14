# Data Extraction Module

The `Data_extraction` module is responsible for loading raw documents, chunking text, generating embeddings, and storing them in the vector database.

## Files

- **`document_loader.py`**: Loads documents from various formats (e.g., PDF, TXT) into LangChain document objects.
- **`text_splitter.py`**: Splits loaded documents into manageable chunks. This step is crucial for staying within LLM context limits and improving retrieval accuracy.
- **`vector_store.py`**: Handles the logic for interacting with the vector database (ChromaDB). It manages embedding models and index building.
- **`ingestion.py`**: The orchestration script that ties the loader, splitter, and vector store together to ingest a new batch of documents.

## Workflow

1. Documents are placed in a target directory or loaded via specific file paths using `document_loader.py`.
2. The `text_splitter.py` breaks these documents into smaller segments using strategies like RecursiveCharacterTextSplitter.
3. Finally, `ingestion.py` uses `vector_store.py` to embed these chunks and insert them into the `chroma_db` for future retrieval.
