import os
import argparse
from Data_extraction.document_loader import DocumentLoader
from Data_extraction.text_splitter import DocumentSplitter
from Data_extraction.vector_store import VectorStoreManager

def run_ingestion(data_dir: str, persist_dir: str, chunk_size: int = 1000, chunk_overlap: int = 200, embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
    """
    Orchestrates the entire ingestion pipeline:
    1. Load documents from data_dir
    2. Split documents into chunks
    3. Store chunks in vector database at persist_dir
    """
    print(f"Starting Medbot Data Ingestion Pipeline...")
    
    # 1. Load Documents
    loader = DocumentLoader(data_dir=data_dir)
    documents = loader.load_documents()
    
    if not documents:
        print("No documents found. Exiting ingestion pipeline.")
        return
        
    # 2. Split Documents
    splitter = DocumentSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    
    # 3. Store in Vector Database
    vector_manager = VectorStoreManager(persist_directory=persist_dir, embedding_model=embedding_model)
    vector_manager.ingest_documents(chunks, batch_size=16)
    
    print("Ingestion Pipeline completed successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Medbot Data Ingestion Pipeline")
    parser.add_argument("--data_dir", type=str, default="./data", help="Directory containing medical documents to ingest")
    parser.add_argument("--persist_dir", type=str, default="./chroma_db", help="Directory to persist the Chroma vector database")
    parser.add_argument("--chunk_size", type=int, default=1000, help="Chunk size for text splitting")
    parser.add_argument("--chunk_overlap", type=int, default=200, help="Chunk overlap for text splitting")
    parser.add_argument("--embedding_model", type=str, default="sentence-transformers/all-MiniLM-L6-v2", help="HuggingFace embedding model to use")
    
    args = parser.parse_args()
    
    run_ingestion(
        data_dir=args.data_dir,
        persist_dir=args.persist_dir,
        chunk_size=args.chunk_size,
        chunk_overlap=args.chunk_overlap,
        embedding_model=args.embedding_model
    )
