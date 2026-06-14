import re
from typing import Set

class HallucinationChecker:
    """
    Performs a lightweight lexical overlap check to detect potential hallucinations.
    """

    def __init__(self, overlap_threshold: float = 0.4):
        self.overlap_threshold = overlap_threshold
        # Extremely basic stop words list
        self.stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "and", "or", "but", "if", 
            "then", "else", "when", "how", "what", "where", "why", "who", "which", 
            "that", "this", "these", "those", "it", "its", "they", "their", "them", 
            "we", "our", "us", "i", "my", "me", "you", "your", "yours", "he", "his", 
            "him", "she", "her", "hers", "to", "of", "in", "for", "on", "with", "as", 
            "by", "at", "from", "about", "into", "through", "during", "before", "after",
            "not", "no", "can", "could", "will", "would", "should", "may", "might", "must",
            "have", "has", "had", "do", "does", "did", "be", "been", "being"
        }

    def _get_significant_words(self, text: str) -> Set[str]:
        # Lowercase and extract alphanumeric words
        words = re.findall(r'\b[a-z0-9]+\b', text.lower())
        # Filter out stop words
        return set([w for w in words if w not in self.stop_words])

    def is_grounded(self, answer: str, context: str) -> bool:
        """
        Returns True if the answer appears grounded in the context based on lexical overlap.
        """
        if not answer.strip():
            return True
            
        if not context.strip():
            return False

        answer_words = self._get_significant_words(answer)
        context_words = self._get_significant_words(context)

        if not answer_words:
            return True # Nothing significant to hallucinate

        # Calculate overlap
        overlap = answer_words.intersection(context_words)
        overlap_percentage = len(overlap) / len(answer_words)

        return overlap_percentage >= self.overlap_threshold
