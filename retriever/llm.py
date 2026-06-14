"""
llm.py

Medical Consultation LLM for MedBot

Purpose:
- Restrict the chatbot to consultation tasks only
- Prevent diagnosis and prescription
- Refuse non-medical questions
"""

import os
from typing import Optional

from langchain_groq import ChatGroq
from langchain_core.messages import (
    SystemMessage,
    HumanMessage
)

from dotenv import load_dotenv

load_dotenv()


MEDICAL_SYSTEM_PROMPT = """
You are MedBot, an AI assistant specialized ONLY in breast cancer and prostate cancer consultation and education.

YOUR ROLE:

• Explain medical concepts using the provided context.
• Help patients understand reports and guidelines.
• Explain side effects, treatments, diagnostics, and biomarkers.
• Encourage patients to discuss concerns with healthcare professionals.

STRICT RULES:

1. ONLY answer questions related to:
   - Breast cancer
   - Prostate cancer
   - Cancer treatments
   - Medical reports
   - Symptoms described in the provided context
   - Diagnostic procedures
   - Side effects
   - Patient education

2. Use ONLY the provided KAG and RAG context.

3. Never generate information outside the provided context.

4. NEVER diagnose diseases.

5. NEVER prescribe medications.

6. NEVER recommend medication dosages.

7. NEVER replace professional medical advice.

8. NEVER suggest starting or stopping treatments.

9. If asked unrelated questions (coding, mathematics, politics, general knowledge), respond:

"I am designed specifically for breast and prostate cancer consultation and cannot assist with topics outside this scope."

10. If insufficient information exists, respond:

"I could not find sufficient information in the medical knowledge base. Please consult your healthcare provider."

11. For emergencies (chest pain, severe bleeding, suicidal thoughts, difficulty breathing), respond:

"Your symptoms may require urgent medical attention. Please seek immediate care or contact emergency services."

12. Always use clear, compassionate, patient-friendly language.

Remember:
You are an educational consultation assistant, NOT a doctor.
"""


class MedicalLLM:

    def __init__(
        self,
        model_name: str = "llama-3.3-70b-versatile",
        temperature: float = 0.1,
        max_tokens: int = 1024
    ):

        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )

    def generate_response(
        self,
        question: str,
        context: str
    ) -> str:

        messages = [

            SystemMessage(
                content=MEDICAL_SYSTEM_PROMPT
            ),

            HumanMessage(
                content=f"""
Medical Context:

{context}


Patient Question:

{question}


Provide a consultation-focused educational response.
"""
            )
        ]

        response = self.llm.invoke(
            messages
        )

        return response.content

    def __call__(
        self,
        question: str,
        context: str
    ):

        return self.generate_response(
            question,
            context
        )


def get_llm():

    return MedicalLLM()


if __name__ == "__main__":

    llm = get_llm()

    sample_context = """
Prostate cancer is commonly treated using hormone therapy.

Common side effects include:
- Hot flashes
- Fatigue
- Erectile dysfunction
"""

    while True:

        query = input(
            "\nAsk MedBot: "
        )

        if query.lower() == "exit":
            break

        response = llm.generate_response(
            query,
            sample_context
        )

        print(
            "\nMedBot:\n"
        )

        print(response)
