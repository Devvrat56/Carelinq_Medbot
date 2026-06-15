import json
import os
from datetime import datetime

class AuditLogger:
    def __init__(self, log_file: str = "audit_log.jsonl"):
        self.log_file = log_file

    def log_interaction(self, patient_id: str, query: str, response: str, sources: list, confidence: float, model_used: str, safety_decision: bool, hallucination_score: float):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "patient_id": patient_id,
            "query": query,
            "response": response,
            "sources": sources,
            "confidence": confidence,
            "model_used": model_used,
            "safety_decision": safety_decision,
            "hallucination_score": hallucination_score
        }
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
