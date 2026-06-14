import torch
from sentence_transformers import CrossEncoder

class BGEReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-base", top_n: int = 3):
        # Initialize the cross-encoder reranker
        self.tokenizer = None # CrossEncoder handles tokenization under the hood
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = CrossEncoder(model_name, max_length=512)
        self.top_n = top_n

    def rerank(self, query: str, retrieved_docs: list[str]) -> list[str]:
        """
        Reranks a list of retrieved documents based on the query.
        Returns the top_n documents.
        """
        if not retrieved_docs:
            return []

        # Create pairs of (query, document) for the cross-encoder
        pairs = [[query, doc] for doc in retrieved_docs]
        
        # Compute scores (higher means more relevant)
        scores = self.model.predict(pairs)
        
        # Sort documents in descending order of their relevance scores
        scored_docs = sorted(zip(retrieved_docs, scores), key=lambda x: x[1], reverse=True)
        
        # Extract and return the top N documents
        ranked_docs = [doc for doc, score in scored_docs[:self.top_n]]
        return ranked_docs
