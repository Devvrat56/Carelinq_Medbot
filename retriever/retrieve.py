"""
retriever.py

Medical RAG Retriever for MedBot

Responsibilities:
- Connect to Chroma Vector Store
- Load HuggingFace Embedding Model
- Retrieve relevant chunks
- Support similarity and MMR search
- Support metadata filtering
- Return source information
"""

import logging
from typing import List, Optional, Dict, Any

from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class MedicalRetriever:
    """
    Retriever class for MedBot.
    """

    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        search_type: str = "mmr",
        k: int = 5,
        fetch_k: int = 20,
    ):

        self.persist_directory = persist_directory
        self.search_type = search_type
        self.k = k
        self.fetch_k = fetch_k

        logging.info(
            f"Loading embedding model: {embedding_model}"
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )

        logging.info(
            f"Connecting to Chroma DB: {persist_directory}"
        )

        self.vector_store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings,
        )

        logging.info(
            "Retriever initialized successfully."
        )

    def retrieve(
        self,
        query: str,
        k: Optional[int] = None,
        filter_metadata: Optional[
            Dict[str, Any]
        ] = None,
    ) -> List[Document]:
        """
        Retrieve relevant documents.

        Parameters
        ----------
        query : str
            User query

        k : int
            Number of documents to return

        filter_metadata : dict
            Optional metadata filters

        Returns
        -------
        List[Document]
        """

        k = k or self.k

        logging.info(
            f"Retrieving documents for: {query}"
        )

        try:

            if self.search_type == "mmr":

                docs = (
                    self.vector_store.max_marginal_relevance_search(
                        query=query,
                        k=k,
                        fetch_k=self.fetch_k,
                        filter=filter_metadata,
                    )
                )

            else:

                docs = (
                    self.vector_store.similarity_search(
                        query=query,
                        k=k,
                        filter=filter_metadata,
                    )
                )

            logging.info(
                f"Retrieved {len(docs)} chunks."
            )

            return docs

        except Exception as e:

            logging.error(
                f"Retrieval failed: {e}"
            )

            return []

    def retrieve_with_scores(
        self,
        query: str,
        k: Optional[int] = None,
        filter_metadata: Optional[
            Dict[str, Any]
        ] = None,
    ):
        """
        Retrieve documents with similarity scores.
        """

        k = k or self.k

        try:

            results = (
                self.vector_store.similarity_search_with_score(
                    query=query,
                    k=k,
                    filter=filter_metadata,
                )
            )

            return results

        except Exception as e:

            logging.error(
                f"Retrieval failed: {e}"
            )

            return []

    def format_sources(
        self,
        docs: List[Document]
    ) -> List[Dict]:

        sources = []

        for doc in docs:

            metadata = doc.metadata

            sources.append(
                {
                    "source": metadata.get(
                        "source",
                        "Unknown",
                    ),
                    "page": metadata.get(
                        "page",
                        "N/A",
                    ),
                    "chunk_id": metadata.get(
                        "chunk_id",
                        "N/A",
                    ),
                }
            )

        return sources

    def print_results(
        self,
        docs: List[Document]
    ):

        print("\n" + "=" * 80)

        for i, doc in enumerate(docs, start=1):

            metadata = doc.metadata

            print(f"\nResult {i}")

            print(
                f"Source: "
                f"{metadata.get('source', 'Unknown')}"
            )

            print(
                f"Page: "
                f"{metadata.get('page', 'N/A')}"
            )

            print(
                f"Chunk ID: "
                f"{metadata.get('chunk_id', 'N/A')}"
            )

            print("\nContent:")

            print(
                doc.page_content[:1000]
            )

            print("\n" + "-" * 80)

    def get_collection_stats(self):

        try:

            count = (
                self.vector_store._collection.count()
            )

            return {
                "total_chunks": count,
                "persist_directory":
                    self.persist_directory,
                "search_type":
                    self.search_type,
            }

        except Exception as e:

            logging.error(
                f"Failed to fetch stats: {e}"
            )

            return {}


if __name__ == "__main__":

    retriever = MedicalRetriever(
        persist_directory="./chroma_db",
        embedding_model=(
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        ),
        search_type="mmr",
        k=5,
    )

    print(
        "\nMedical Retriever Ready!"
    )

    stats = retriever.get_collection_stats()

    print(
        f"\nIndexed Chunks: "
        f"{stats.get('total_chunks', 0)}"
    )

    while True:

        query = input(
            "\nEnter medical query "
            "(or 'exit'): "
        )

        if query.lower() == "exit":
            break

        documents = (
            retriever.retrieve(query)
        )

        retriever.print_results(
            documents
        )

        print("\nSources:")

        print(
            retriever.format_sources(
                documents
            )
        )