from typing import List, Dict, Any
from langchain_core.documents import Document

class CitationManager:
    """
    Handles formatting of document citations into structured JSON and formatted text.
    """

    def format_citations(self, docs: List[Document]) -> Dict[str, Any]:
        if not docs:
            return {
                "structured": [],
                "formatted_text": "No sources retrieved."
            }

        structured = []
        formatted_lines = ["Sources:"]

        # Track unique sources to avoid redundant citations
        seen_sources = set()

        for idx, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "Unknown Document")
            page = doc.metadata.get("page", "N/A")
            
            citation_key = f"{source}_p{page}"
            
            if citation_key not in seen_sources:
                seen_sources.add(citation_key)
                
                structured.append({
                    "source": source,
                    "page": page
                })
                
                formatted_lines.append(f"{idx}. {source} (Page {page})")

        return {
            "structured": structured,
            "formatted_text": "\n".join(formatted_lines)
        }
