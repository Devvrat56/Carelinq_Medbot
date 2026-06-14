from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentSplitter:
    """Handles chunking of large documents into smaller, processable pieces."""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Splits a list of documents into smaller chunks."""
        if not documents:
            return []
            
        print(f"Splitting {len(documents)} documents into chunks...")
        chunks = self.splitter.split_documents(documents)
        print(f"Created {len(chunks)} chunks.")
        return chunks
