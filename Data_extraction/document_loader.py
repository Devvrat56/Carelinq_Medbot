import os
import glob
import json
from typing import List
from langchain_community.document_loaders import PyPDFLoader, TextLoader, CSVLoader
from langchain_core.documents import Document

class DocumentLoader:
    """Handles the loading of various document types for the ingestion pipeline."""
    
    def __init__(self, data_dir: str):
        self.data_dir = data_dir

    def load_documents(self) -> List[Document]:
        """
        Loads all supported documents from the configured data directory.
        Currently supports: .json (pre-extracted), .pdf, .txt, .csv
        """
        documents = []
        if not os.path.exists(self.data_dir):
            print(f"Warning: Directory {self.data_dir} does not exist.")
            return documents

        for file_path in glob.glob(os.path.join(self.data_dir, "**/*.*"), recursive=True):
            try:
                if file_path.lower().endswith(".json"):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Extract the text and create a Document object
                        text_content = data.get("text", "")
                        metadata = data.get("metadata", {})
                        metadata["source"] = data.get("filename", file_path)
                        metadata["absolute_path"] = data.get("absolute_path", file_path)
                        
                        doc = Document(page_content=text_content, metadata=metadata)
                        documents.append(doc)
                elif file_path.lower().endswith(".pdf"):
                    loader = PyPDFLoader(file_path)
                    documents.extend(loader.load())
                elif file_path.lower().endswith(".txt"):
                    loader = TextLoader(file_path, encoding='utf-8')
                    documents.extend(loader.load())
                elif file_path.lower().endswith(".csv"):
                    loader = CSVLoader(file_path)
                    documents.extend(loader.load())
                else:
                    print(f"Skipping unsupported file format: {file_path}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")

        print(f"Successfully loaded {len(documents)} document pages/chunks from {self.data_dir}")
        return documents
