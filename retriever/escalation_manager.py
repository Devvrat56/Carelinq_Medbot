class EscalationManager:
    def __init__(self, confidence_threshold: float = 0.5, hallucination_threshold: float = 0.6):
        self.confidence_threshold = confidence_threshold
        self.hallucination_threshold = hallucination_threshold
        self.emergency_keywords = ["emergency", "suicide", "heart attack", "stroke", "bleeding profusely"]

    def should_escalate(self, query: str, confidence: float, hallucination_score: float) -> bool:
        if confidence < self.confidence_threshold:
            return True
            
        if hallucination_score < self.hallucination_threshold:
            return True
            
        query_lower = query.lower()
        for keyword in self.emergency_keywords:
            if keyword in query_lower:
                return True
                
        return False

    def get_escalation_message(self) -> str:
        return "I recommend discussing this question immediately with your healthcare provider or seeking emergency medical attention if necessary."
