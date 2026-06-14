# rag_pipeline.py

from retriever import MedicalRetriever
from llm import get_llm
from prompts import SYSTEM_PROMPT
from safety import detect_emergency

from langchain_core.prompts import PromptTemplate


class MedicalRAG:

    def __init__(self):

        self.retriever = MedicalRetriever()

        self.llm = get_llm()

        self.prompt = PromptTemplate(
            input_variables=[
                "context",
                "question"
            ],
            template=SYSTEM_PROMPT
        )

    def retrieve_context(
        self,
        query
    ):

        docs = retriever.retrieve(query, k=20)

        reranked_docs = reranker.rerank(
    query=query,
    documents=docs,
    top_k=5
)

        context = "\n\n".join(

            f"Source: "
            f"{doc.metadata.get('source')} "
            f"(Page {doc.metadata.get('page')})\n"
            f"{doc.page_content}"

            for doc in docs
        )

        return context, docs

    def generate_answer(
        self,
        question
    ):

        if detect_emergency(question):

            return {

                "answer":
                (
                    "Your symptoms may "
                    "require urgent medical "
                    "attention. Please "
                    "contact emergency "
                    "services or your "
                    "healthcare provider "
                    "immediately."
                ),

                "sources": []
            }

        context, docs = (
            self.retrieve_context(
                question
            )
        )

        if not context:

            return {

                "answer":
                (
                    "I could not find "
                    "relevant information "
                    "in the medical "
                    "knowledge base."
                ),

                "sources": []
            }

        prompt = self.prompt.format(

            context=context,

            question=question
        )

        response = self.llm.invoke(
            prompt
        )

        sources = (

            self.retriever.format_sources(
                docs
            )
        )

        return {

            "answer":
            response.content,

            "sources":
            sources
        }


if __name__ == "__main__":

    rag = MedicalRAG()

    while True:

        query = input(
            "\nAsk MedBot: "
        )

        if query.lower() == "exit":
            break

        response = (
            rag.generate_answer(
                query
            )
        )

        print(
            "\nAnswer:\n"
        )

        print(
            response["answer"]
        )

        print(
            "\nSources:"
        )

        for source in (
            response["sources"]
        ):

            print(source)