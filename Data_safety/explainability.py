class ExplainabilityLayer:
    def __init__(self):
        pass

    def generate_explanation(self, answer: str, kg_facts_used: list, retrieved_chunks: list, confidence_score: float) -> dict:
        explanation = {
            "answer": answer,
            "reasoning": [],
            "confidence_score": confidence_score
        }
        
        for fact in kg_facts_used:
            explanation["reasoning"].append(f"KG: {fact}")
            
        for chunk in retrieved_chunks:
            explanation["reasoning"].append(f"Document: {chunk.get('source', 'Unknown')} Page {chunk.get('page', 'Unknown')}")
            
        return explanation
