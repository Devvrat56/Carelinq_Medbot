import base64
import urllib.request

graph = """flowchart TD
    User([User: Patient/Doctor]) --> API[FastAPI Backend]
    
    subgraph Security
        API --> Auth[JWT Auth]
        Auth --> PII[PII Masking]
        PII --> Guard[Clinical Guardrails]
    end
    
    subgraph Processing
        Guard --> Upload[Report Upload]
        Guard --> Chat[Chat Interface]
        
        Upload --> Blob[(Floci Blob)]
        Upload --> OCR[Report Analyzer]
        OCR --> KG_Up[KG Updater]
        
        Chat --> Mem[Memory]
        Mem --> Cache[(Redis Cache)]
        Mem --> RAG[RAG Pipeline]
    end
    
    subgraph Databases
        RAG --> Chroma[(ChromaDB)]
        RAG --> Neo4j[(Neo4j)]
        KG_Up --> Neo4j
    end
    
    subgraph Evaluation
        RAG --> Esc[Escalation]
        Esc --> Explain[Explainability]
        Explain --> Audit[Audit Logger]
        Audit --> API
    end
"""

encoded = base64.b64encode(graph.encode('utf-8')).decode('utf-8')
url = f"https://mermaid.ink/img/{encoded}?bgColor=white"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req) as response, open('architecture.png', 'wb') as out_file:
        out_file.write(response.read())
    print("architecture.png created successfully!")
except Exception as e:
    print(f"Error: {e}")
