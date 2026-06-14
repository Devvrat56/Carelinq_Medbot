import math
from typing import List

class ConfidenceScorer:
    """
    Calculates a blended confidence score using retriever distances and reranker logits.
    """

    def __init__(self, retriever_weight: float = 0.3, reranker_weight: float = 0.7):
        self.retriever_weight = retriever_weight
        self.reranker_weight = reranker_weight

    def _sigmoid(self, x: float) -> float:
        try:
            return 1 / (1 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def calculate_confidence(self, retriever_scores: List[float], reranker_scores: List[float]) -> float:
        if not retriever_scores or not reranker_scores:
            return 0.0

        # Heuristic: Average the top 3 scores
        top_k = min(3, len(retriever_scores), len(reranker_scores))
        
        # Normalize retriever scores (Assuming L2 distance from Chroma where lower is better)
        # We invert it: 1 / (1 + distance)
        avg_retriever_dist = sum(retriever_scores[:top_k]) / top_k
        norm_retriever_score = 1 / (1 + avg_retriever_dist)

        # Normalize reranker scores (Cross-Encoder logits) via Sigmoid
        avg_reranker_logit = sum(reranker_scores[:top_k]) / top_k
        norm_reranker_score = self._sigmoid(avg_reranker_logit)

        # Blend
        confidence = (norm_retriever_score * self.retriever_weight) + (norm_reranker_score * self.reranker_weight)
        
        # Return as a percentage rounded to 2 decimal places
        return round(confidence * 100, 2)
