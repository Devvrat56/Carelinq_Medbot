from Data_safety.pii_detector import PIIDetector

class Deidentifier:
    def __init__(self):
        self.detector = PIIDetector()

    def deidentify(self, text: str) -> str:
        findings = self.detector.detect_pii(text)
        
        # Sort findings by start index descending to avoid offset issues when replacing
        findings.sort(key=lambda x: x["start"], reverse=True)
        
        deidentified_text = text
        for finding in findings:
            start = finding["start"]
            end = finding["end"]
            entity_type = finding["entity_type"]
            
            deidentified_text = deidentified_text[:start] + f"[{entity_type}]" + deidentified_text[end:]
            
        return deidentified_text
