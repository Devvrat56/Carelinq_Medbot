import base64
import urllib.request

graph = """sequenceDiagram
    actor U as User
    participant A as FastAPI
    participant S as Safety & PII
    participant B as Floci Blob
    participant M as Memory
    participant R as Retrieval Pipeline
    participant DB as Databases
    participant L as LLM Router
    participant E as Eval & Audit
    
    rect rgb(240, 248, 255)
        note right of U: Document Upload Workflow
        U->>A: POST /upload-report
        A->>A: JWT Auth Check
        A->>B: Upload PDF to Emulated Azure Blob
        A->>R: Analyze Medical Report
        R->>DB: Store Embeddings (Chroma) & Triples (Neo4j)
        A-->>U: Return Summary
    end

    rect rgb(255, 245, 238)
        note right of U: Chat Workflow
        U->>A: POST /chat
        A->>A: JWT Auth Check
        A->>S: Mask PII & Apply Guardrails
        S->>M: Get Summarized Chat History
        M->>R: Send Masked Query
        R->>DB: Vector Search & Graph Traversal
        R->>R: Cross-Encoder Rerank
        R->>L: Prompt LLM (Fallback: Groq->OpenAI)
        L-->>R: Generated Response
        R->>E: Score Confidence & Hallucination
        E->>E: Check Escalation Thresholds
        E->>E: Attach Citations & Explainability
        E->>E: Write to Audit Log (audit_logger.py)
        E-->>U: Return Final Safe Answer
    end
"""

encoded = base64.b64encode(graph.encode('utf-8')).decode('utf-8')
url = f"https://mermaid.ink/img/{encoded}?bgColor=white"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response, open('workflow_architecture.png', 'wb') as out_file:
        out_file.write(response.read())
    print("workflow_architecture.png created successfully!")
except Exception as e:
    print(f"Error: {e}")
