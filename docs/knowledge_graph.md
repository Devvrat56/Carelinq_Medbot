# Knowledge Graph Module

The `knowledge_graph` module extends the standard RAG setup by injecting structured, relationship-based medical knowledge (Knowledge-Augmented Generation - KAG).

## Files

- **`entity_extractor.py`**: Uses NLP models (specifically `scispacy` models like `en_core_sci_sm`) to extract medical entities (diseases, symptoms, medications) and their relationships from text.
- **`graph_builder.py`**: Constructs a mathematical graph of these entities using `NetworkX`. It creates nodes for entities and edges for their relationships (e.g., `Prostate Cancer` -> `TREATED_WITH` -> `Hormone Therapy`).
- **`graph_retriever.py`**: Provides search functionalities over the built graph. Given a clinical query, it traverses the graph to pull relevant structured triples (Subject-Predicate-Object) to feed into the generation pipeline.

## Why a Knowledge Graph?

While Vector databases excel at semantic similarity, Knowledge Graphs excel at preserving exact factual relationships. By combining both (KAG + RAG), the chatbot significantly reduces hallucinations on exact medical treatments and diagnosis guidelines.
