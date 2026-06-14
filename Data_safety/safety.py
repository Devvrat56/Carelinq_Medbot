"""
safety.py

Medical safety layer for MedBot.

Responsibilities:
- Emergency detection
- Domain restriction
- Diagnosis prevention
- Prescription prevention
"""

import re
from typing import Dict


class MedicalSafetyChecker:

    def __init__(self):

        self.emergency_keywords = {

            "chest pain",
            "difficulty breathing",
            "shortness of breath",
            "suicidal",
            "suicide",
            "severe bleeding",
            "loss of consciousness",
            "stroke",
            "heart attack",
            "seizure",
            "fainted",
            "collapsed"
        }

        self.diagnosis_patterns = [

            r"\bdo i have\b",
            r"\bcan you diagnose\b",
            r"\bwhat disease do i have\b",
            r"\bdo i have cancer\b",
            r"\bwhat is my diagnosis\b",
            r"\bam i suffering from\b"
        ]

        self.prescription_patterns = [

            r"\bwhat medication should i take\b",
            r"\bprescribe\b",
            r"\bwhat dose\b",
            r"\bdosage\b",
            r"\bhow much medicine\b",
            r"\bshould i stop taking\b",
            r"\bshould i start taking\b"
        ]

        self.treatment_decision_patterns = [

            r"\bwhich treatment is best\b",
            r"\bshould i undergo surgery\b",
            r"\bshould i take chemotherapy\b",
            r"\bshould i choose radiation\b",
            r"\bwhat treatment should i choose\b"
        ]

        self.allowed_topics = {

            "breast cancer",
            "prostate cancer",
            "psa",
            "gleason",
            "her2",
            "hormone therapy",
            "chemotherapy",
            "radiation therapy",
            "trastuzumab",
            "biopsy",
            "mammogram",
            "pathology report",
            "side effects",
            "symptoms",
            "treatment",
            "diagnosis",
            "cancer"
        }

    def detect_emergency(
        self,
        query: str
    ) -> bool:

        query = query.lower()

        return any(

            keyword in query

            for keyword in self.emergency_keywords
        )

    def detect_diagnosis_request(
        self,
        query: str
    ) -> bool:

        query = query.lower()

        return any(

            re.search(
                pattern,
                query
            )

            for pattern in self.diagnosis_patterns
        )

    def detect_prescription_request(
        self,
        query: str
    ) -> bool:

        query = query.lower()

        return any(

            re.search(
                pattern,
                query
            )

            for pattern in self.prescription_patterns
        )

    def detect_treatment_decision_request(
        self,
        query: str
    ) -> bool:

        query = query.lower()

        return any(

            re.search(
                pattern,
                query
            )

            for pattern in self.treatment_decision_patterns
        )

    def detect_out_of_scope(
        self,
        query: str
    ) -> bool:

        query = query.lower()

        return not any(

            topic in query

            for topic in self.allowed_topics
        )

    def evaluate(
        self,
        query: str
    ) -> Dict:

        if self.detect_emergency(
            query
        ):

            return {

                "allowed": False,

                "category": "emergency",

                "message": (
                    "Your symptoms may require "
                    "urgent medical attention. "
                    "Please contact emergency "
                    "services or seek immediate "
                    "medical care."
                )
            }

        if self.detect_diagnosis_request(
            query
        ):

            return {

                "allowed": False,

                "category": "diagnosis",

                "message": (
                    "I cannot diagnose medical "
                    "conditions. Please consult "
                    "a qualified healthcare "
                    "professional for diagnosis."
                )
            }

        if self.detect_prescription_request(
            query
        ):

            return {

                "allowed": False,

                "category": "prescription",

                "message": (
                    "I cannot prescribe "
                    "medications or recommend "
                    "dosages. Please consult "
                    "your healthcare provider."
                )
            }

        if self.detect_treatment_decision_request(
            query
        ):

            return {

                "allowed": False,

                "category": "treatment_decision",

                "message": (
                    "Treatment decisions should "
                    "be made with your oncology "
                    "team. I can provide "
                    "educational information "
                    "about available treatments."
                )
            }

        if self.detect_out_of_scope(
            query
        ):

            return {

                "allowed": False,

                "category": "out_of_scope",

                "message": (
                    "I specialize in breast "
                    "and prostate cancer "
                    "consultation and cannot "
                    "assist with unrelated "
                    "topics."
                )
            }

        return {

            "allowed": True,

            "category": "safe",

            "message": None
        }


if __name__ == "__main__":

    safety = MedicalSafetyChecker()

    while True:

        query = input(
            "\nQuery: "
        )

        if query.lower() == "exit":
            break

        result = safety.evaluate(
            query
        )

        print(result)
