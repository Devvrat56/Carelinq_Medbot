class ClinicalGuardrails:
    def __init__(self):
        # Keywords that should trigger guardrails
        self.forbidden_keywords = [
            "prescribe", "dosage", "diagnose", "prognosis", "cure", "treatment recommendation"
        ]

    def is_safe(self, query: str) -> bool:
        query_lower = query.lower()
        for keyword in self.forbidden_keywords:
            if keyword in query_lower:
                return False
        return True
        
    def get_guardrail_response(self) -> str:
        return "As an AI assistant, I am not authorized to provide medical diagnoses, treatment recommendations, or medication dosages. Please consult with a qualified healthcare provider."
