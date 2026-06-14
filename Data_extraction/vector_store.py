# vector_store.py

import os
import os
import json
import hashlib
import logging
from typing import List

os.environ["OMP_NUM_THREADS"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
torch.set_num_threads(1)

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class VectorStoreManager:
    """
    Handles embedding generation and Chroma persistence.
    """

    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
    ):

        self.persist_directory = persist_directory

        self.manifest_path = os.path.join(
            persist_directory,
            "manifest.json"
        )

        os.makedirs(
            persist_directory,
            exist_ok=True
        )

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

    def _load_manifest(self):

        if os.path.exists(self.manifest_path):

            with open(
                self.manifest_path,
                "r"
            ) as f:

                return json.load(f)

        return {
            "processed_files": []
        }

    def _save_manifest(
        self,
        manifest
    ):

        with open(
            self.manifest_path,
            "w"
        ) as f:

            json.dump(
                manifest,
                f,
                indent=4
            )

    def remove_duplicates(
        self,
        documents: List[Document]
    ) -> List[Document]:

        unique_docs = []
        seen_hashes = set()

        for doc in documents:

            content = doc.page_content.strip()

            if len(content) < 50:
                continue

            content_hash = hashlib.md5(
                content.encode()
            ).hexdigest()

            if content_hash not in seen_hashes:

                seen_hashes.add(content_hash)
                unique_docs.append(doc)

        logging.info(
            f"Removed duplicates. "
            f"{len(unique_docs)} unique chunks remain."
        )

        return unique_docs

    def assign_chunk_ids(
        self,
        documents: List[Document]
    ):

        for idx, doc in enumerate(documents):

            source = doc.metadata.get(
                "source",
                "unknown"
            )

            page = doc.metadata.get(
                "page",
                0
            )

            chunk_id = (
                f"{os.path.basename(source)}"
                f"_p{page}"
                f"_c{idx}"
            )

            doc.metadata["chunk_id"] = chunk_id

        return documents

    def filter_processed_files(
        self,
        documents: List[Document]
    ):

        manifest = self._load_manifest()

        processed = set(
            manifest["processed_files"]
        )

        filtered_docs = []

        for doc in documents:

            source = doc.metadata.get(
                "source",
                "unknown"
            )

            if source not in processed:

                filtered_docs.append(doc)

        return filtered_docs

    def update_manifest(
        self,
        documents: List[Document]
    ):

        manifest = self._load_manifest()

        processed = set(
            manifest["processed_files"]
        )

        for doc in documents:

            source = doc.metadata.get(
                "source",
                "unknown"
            )

            processed.add(source)

        manifest["processed_files"] = list(
            processed
        )

        self._save_manifest(manifest)

    def ingest_documents(
        self,
        documents: List[Document],
        batch_size: int = 100
    ):

        logging.info(
            f"Received {len(documents)} chunks."
        )

        documents = self.remove_duplicates(
            documents
        )

        documents = self.assign_chunk_ids(
            documents
        )

        documents = self.filter_processed_files(
            documents
        )

        if len(documents) == 0:

            logging.info(
                "No new documents to ingest."
            )

            return

        logging.info(
            f"Ingesting {len(documents)} chunks via Chroma.from_documents to prevent OS segmentation faults..."
        )
        
        # Sanitize metadata to prevent ChromaDB SQLite segfaults
        for doc in documents:
            clean_meta = {}
            for k, v in doc.metadata.items():
                if isinstance(v, (str, int, float, bool)):
                    clean_meta[k] = v
                elif v is not None:
                    clean_meta[k] = str(v)
            doc.metadata = clean_meta

        # Bypassing the add_documents loop and using the stable classmethod instead
        Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory
        )

        self.update_manifest(
            documents
        )

        logging.info(
            "Ingestion completed successfully."
        )

    def get_stats(self):

        count = self.vector_db._collection.count()

        return {
            "total_chunks": count,
            "persist_directory":
                self.persist_directory
        }
