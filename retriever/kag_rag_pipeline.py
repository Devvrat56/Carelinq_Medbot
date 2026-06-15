"""
kag_rag_pipeline.py

Hybrid Knowledge-Augmented Generation +
Retrieval-Augmented Generation pipeline with
integrated Safety and Advanced Patient Memory.
"""

import logging

from Data_safety.safety import MedicalSafetyChecker
from knowledge_graph.graph_retriever import GraphRetriever
from retriever.retrieve import MedicalRetriever
from retriever.reranker import BGEReranker as MedicalReranker
from retriever.memory import PatientMemoryManager
from retriever.llm import get_llm
from context import init_conversation as general_context
from context2 import get_system_prompt as symptom_context

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class KAGRAGPipeline:

    def __init__(self):
        print("Initializing Safety Layer...")
        self.safety = MedicalSafetyChecker()

        print("Initializing KAG Retriever...")
        self.kag = GraphRetriever()

        print("Initializing RAG Retriever...")
        self.rag = MedicalRetriever(
            search_type="mmr",
            k=10
        )

        print("Initializing Reranker...")
        self.reranker = MedicalReranker()

        print("Initializing LLM...")
        self.llm = get_llm()
        
        print("Initializing Patient Memory...")
        self.memory = PatientMemoryManager("medbot_patients.db")

    def retrieve_knowledge_graph_context(self, query):
        try:
            knowledge = self.kag.retrieve_knowledge(query)
            if not knowledge:
                return ""
            return self.kag.format_knowledge(knowledge)
        except Exception as e:
            logging.error(f"KAG Retrieval failed: {e}")
            return ""

    def retrieve_rag_context(self, query):
        try:
            docs = self.rag.retrieve(query, k=15)
            
            if not docs:
                return "", []

            docs = self.reranker.rerank(
                query=query,
                retrieved_docs=docs
            )

            context = "\n\n".join([
                f"Source: {doc.metadata.get('source')} (Page {doc.metadata.get('page')})\n{doc.page_content}"
                for doc in docs
            ])
            return context, docs
        except Exception as e:
            logging.error(f"RAG Retrieval failed: {e}")
            return "", []

    def build_prompt(self, query, kag_context, rag_context, chat_history, patient_context):
        # 1. Format Chat History
        history_text = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in chat_history])
        if not history_text:
            history_text = "No previous history."

        # 2. Format Patient Profile
        patient_info = "No specific patient profile available."
        if patient_context:
            patient_info = f"""
Patient Information:
- Age: {patient_context.get('age', 'N/A')}
- Gender: {patient_context.get('gender', 'N/A')}
- Diagnosis: {patient_context.get('diagnosis', 'N/A')}
- PSA Level: {patient_context.get('psa_level', 'N/A')}
- Gleason Score: {patient_context.get('gleason_score', 'N/A')}
- Current Treatment: {patient_context.get('current_treatment', 'N/A')}
- Allergies: {patient_context.get('allergies', 'N/A')}
"""

        # 3. Compile Master Prompt
        symptom_keywords = ['pain', 'hurt', 'lump', 'bleeding', 'tired', 'fatigue', 'fever', 'sweats', 'weight', 'symptom', 'ache', 'swelling', 'nausea', 'vomit', 'cough', 'feel']
        is_symptom = any(kw in query.lower() for kw in symptom_keywords)
        base_prompt = symptom_context() if is_symptom else general_context

        return f"""{base_prompt}

ADDITIONAL RULES FOR THIS QUERY:
1. Use BOTH the structured knowledge graph information and retrieved medical documents.
2. Adapt your answer based on the Patient Information provided (e.g. referencing their PSA or Treatment if relevant).
3. If information is insufficient, say: "I could not find sufficient information in the medical knowledge base."

{patient_info}

Recent Conversation:
{history_text}

Knowledge Graph Information:
{kag_context}

Retrieved Medical Context:
{rag_context}

User Question:
{query}

Provide a structured and educational answer:
"""

    def answer(self, query, patient_id=None):
        # 1. Safety Check
        safety_eval = self.safety.evaluate(query)
        if not safety_eval.get("allowed", False):
            return {
                "answer": safety_eval.get("message", "Request blocked by safety policy."),
                "knowledge_graph": "",
                "sources": [],
                "safety": safety_eval
            }

        # 2. Retrieve Patient Memory
        patient_context = {}
        chat_history = []
        if patient_id:
            patient_context = self.memory.get_patient_context(patient_id)
            chat_history = self.memory.get_recent_history(patient_id, limit=5)

        # 3. KAG and RAG Retrieval
        kag_context = self.retrieve_knowledge_graph_context(query)
        rag_context, docs = self.retrieve_rag_context(query)

        # 4. Prompt Construction & LLM Generation
        prompt = self.build_prompt(
            query=query,
            kag_context=kag_context,
            rag_context=rag_context,
            chat_history=chat_history,
            patient_context=patient_context
        )

        try:
            # We send the fully populated prompt into the 'context' block of generate_response
            response_content = self.llm.generate_response(
                question=query,
                context=prompt
            )
        except Exception as e:
            logging.error(f"LLM Generation failed: {e}")
            response_content = "An error occurred while generating the response. Please try again."

        # 5. Format Sources
        sources = []
        if docs:
            for doc in docs:
                sources.append({
                    "source": doc.metadata.get("source"),
                    "page": doc.metadata.get("page")
                })

        # 6. Save to Memory
        if patient_id:
            try:
                self.memory.add_message(patient_id, "user", query)
                self.memory.add_message(patient_id, "assistant", response_content)
            except Exception as e:
                logging.error(f"Failed to save to memory: {e}")

        return {
            "answer": response_content,
            "knowledge_graph": kag_context,
            "sources": sources,
            "safety": safety_eval
        }


if __name__ == "__main__":
    chatbot = KAGRAGPipeline()
    dummy_patient_id = "patient_123"

    print("\n[!] Mocking Dummy Patient Profile...")
    chatbot.memory.upsert_patient_profile(
        patient_id=dummy_patient_id,
        name="John Doe",
        age=65,
        gender="Male",
        diagnosis="Prostate Cancer",
        psa_level=8.5,
        gleason_score="7 (3+4)",
        current_treatment="Hormone Therapy",
        allergies="Penicillin"
    )

    print("\n[!] Type 'exit' to stop. Pipeline is ready.")

    while True:
        query = input(f"\nAsk MedBot (as {dummy_patient_id}): ")
        if query.lower() == "exit":
            break

        result = chatbot.answer(query, patient_id=dummy_patient_id)

        print("\n--- SAFETY EVAL ---")
        print(f"Status: {result['safety'].get('category', 'unknown')}")

        print("\n--- ANSWER ---")
        print(result["answer"])

        if result["safety"].get("allowed"):
            print("\n--- KAG FACTS ---")
            print(result["knowledge_graph"] if result["knowledge_graph"] else "No exact KAG facts found.")

            print("\n--- RAG SOURCES ---")
            for source in result["sources"]:
                print(f"- {source['source']} (Page {source['page']})")