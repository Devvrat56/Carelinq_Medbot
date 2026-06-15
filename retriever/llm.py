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
You are MedBot, an Advanced Oncology Clinical Assistant.
Follow the strict medical safety guidelines and rules provided in your context.
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
