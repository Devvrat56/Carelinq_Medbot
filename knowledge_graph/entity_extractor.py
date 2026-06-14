"""
entity_extractor.py

Extract medical entities and relationships from text
for Knowledge-Augmented Generation (KAG).

Version 1:
- Rule-based extraction
- Easy to extend
- Works with existing RAG data
"""

import re
from typing import List, Dict


class MedicalEntityExtractor:

    def __init__(self):

        # Disease entities
        self.diseases = {
            "prostate cancer",
            "breast cancer",
            "metastatic prostate cancer",
            "advanced breast cancer"
        }

        # Treatment entities
        self.treatments = {
            "hormone therapy",
            "radiation therapy",
            "chemotherapy",
            "trastuzumab",
            "pertuzumab",
            "surgery",
            "radical prostatectomy",
            "immunotherapy"
        }

        # Diagnostic tests
        self.diagnostic_tests = {
            "psa test",
            "biopsy",
            "mri",
            "mammogram",
            "ultrasound",
            "ct scan",
            "pet scan"
        }

        # Biomarkers
        self.biomarkers = {
            "her2",
            "brca1",
            "brca2",
            "psa",
            "estrogen receptor",
            "progesterone receptor",
            "ki-67"
        }

        # Symptoms
        self.symptoms = {
            "difficulty urinating",
            "blood in urine",
            "bone pain",
            "fatigue",
            "hot flashes",
            "breast lump",
            "weight loss"
        }

        # Side effects
        self.side_effects = {
            "incontinence",
            "erectile dysfunction",
            "nausea",
            "vomiting",
            "hair loss",
            "cardiotoxicity",
            "hot flashes"
        }

    def extract_entities(
        self,
        text: str
    ) -> List[Dict]:

        text = text.lower()

        entities = []

        categories = {

            "Disease": self.diseases,

            "Treatment": self.treatments,

            "Diagnostic Test": self.diagnostic_tests,

            "Biomarker": self.biomarkers,

            "Symptom": self.symptoms,

            "Side Effect": self.side_effects
        }

        for entity_type, values in categories.items():

            for value in values:

                pattern = (
                    r'\b'
                    + re.escape(value)
                    + r'\b'
                )

                if re.search(pattern, text):

                    entities.append({

                        "entity": value.title(),

                        "type": entity_type
                    })

        return entities

    def extract_relationships(
        self,
        text: str,
        entities: List[Dict]
    ):

        text = text.lower()

        relationships = []

        entity_lookup = {

            e["entity"].lower(): e["type"]

            for e in entities
        }

        # Disease -> Treatment
        if any(
            treatment in text
            for treatment in self.treatments
        ):

            for disease in self.diseases:

                if disease in text:

                    for treatment in self.treatments:

                        if treatment in text:

                            relationships.append({

                                "source":
                                    disease.title(),

                                "target":
                                    treatment.title(),

                                "relationship":
                                    "TREATED_WITH"
                            })

        # Disease -> Diagnostic Test
        if any(
            test in text
            for test in self.diagnostic_tests
        ):

            for disease in self.diseases:

                if disease in text:

                    for test in self.diagnostic_tests:

                        if test in text:

                            relationships.append({

                                "source":
                                    disease.title(),

                                "target":
                                    test.title(),

                                "relationship":
                                    "DIAGNOSED_BY"
                            })

        # Treatment -> Side Effect
        if any(
            effect in text
            for effect in self.side_effects
        ):

            for treatment in self.treatments:

                if treatment in text:

                    for effect in self.side_effects:

                        if effect in text:

                            relationships.append({

                                "source":
                                    treatment.title(),

                                "target":
                                    effect.title(),

                                "relationship":
                                    "CAUSES_SIDE_EFFECT"
                            })

        return relationships


if __name__ == "__main__":

    sample_text = """

    Prostate cancer can be diagnosed using PSA test
    and biopsy.

    Hormone therapy is commonly used for advanced
    prostate cancer.

    Hormone therapy may cause hot flashes.

    """

    extractor = MedicalEntityExtractor()

    entities = extractor.extract_entities(
        sample_text
    )

    relationships = (
        extractor.extract_relationships(
            sample_text,
            entities
        )
    )

    print("\nEntities:")

    for entity in entities:

        print(entity)

    print("\nRelationships:")

    for relation in relationships:

        print(relation)
