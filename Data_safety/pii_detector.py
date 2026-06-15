import re

class PIIDetector:
    def __init__(self):
        # Basic regex patterns for PII detection.
        # In a real production system, consider using Microsoft Presidio or a specialized NLP model.
        self.patterns = {
            "EMAIL": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            "PHONE": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
            "SSN": r"\b\d{3}-\d{2}-\d{4}\b",
            "MRN": r"\b(MRN|mrn)[\s:-]*\d+\b",
        }

    def detect_pii(self, text: str) -> list:
        findings = []
        for entity_type, pattern in self.patterns.items():
            for match in re.finditer(pattern, text):
                findings.append({
                    "entity_type": entity_type,
                    "start": match.start(),
                    "end": match.end(),
                    "value": match.group()
                })
        return findings
