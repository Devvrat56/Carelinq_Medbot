import os
import uuid
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
load_dotenv() # Load environment variables from .env if present

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import shutil

# Internal MedBot Modules
from Data_safety.safety import MedicalSafetyChecker
from Data_safety.confidence import ConfidenceScorer
from Data_safety.hallucination_checker import HallucinationChecker
from retriever.citation_manager import CitationManager
from retriever.memory import PatientMemoryManager
from retriever.report_analyzer import MedicalReportAnalyzer
from retriever.kag_rag_pipeline import KAGRAGPipeline
from knowledge_graph.kg_updater import KnowledgeGraphUpdater
from storage.blob_manager import BlobManager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = FastAPI(title="MedBot Consultation API", version="1.0.0")

# CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances (Loaded once at startup)
memory_mgr = PatientMemoryManager("medbot_patients.db")
pipeline = KAGRAGPipeline()
# Pipeline already encapsulates Safety and Retrievers, but we'll instantiate metrics here
confidence_scorer = ConfidenceScorer()
hallucination_checker = HallucinationChecker()
citation_manager = CitationManager()
report_analyzer = MedicalReportAnalyzer()
kg_updater = KnowledgeGraphUpdater()
blob_manager = BlobManager()


# --- Pydantic Models for FastAPI ---
class ChatRequest(BaseModel):
    patient_id: str
    query: str

class PatientCreateRequest(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    diagnosis: str
    psa_level: Optional[float] = None
    gleason_score: Optional[str] = None
    current_treatment: Optional[str] = None
    allergies: Optional[str] = None


# --- FastAPI Endpoints ---

@app.post("/patient")
async def create_patient(req: PatientCreateRequest):
    memory_mgr.upsert_patient_profile(
        patient_id=req.patient_id, name=req.name, age=req.age, gender=req.gender,
        diagnosis=req.diagnosis, psa_level=req.psa_level, gleason_score=req.gleason_score,
        current_treatment=req.current_treatment, allergies=req.allergies
    )
    return {"status": "success", "message": f"Patient {req.patient_id} created/updated."}

@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str):
    profile = memory_mgr.get_patient_context(patient_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Patient not found.")
    history = memory_mgr.get_recent_history(patient_id, limit=10)
    return {"profile": profile, "history": history}

@app.post("/upload-report")
async def upload_report(patient_id: str = Form(...), file: UploadFile = File(...)):
    if not memory_mgr.get_patient_context(patient_id):
        raise HTTPException(status_code=404, detail="Patient not found. Create patient first.")

    temp_path = f"temp_{file.filename}"
    try:
        # Upload to Azure Blob Storage (Floci Emulator)
        file_bytes = await file.read()
        try:
            blob_manager.upload_report(file.filename, file_bytes)
        except Exception as e:
            logging.warning(f"Failed to upload to Azure Blob Storage (Is Floci running?): {e}")

        # Write to temp file for local processing
        with open(temp_path, "wb") as buffer:
            buffer.write(file_bytes)
            
        raw_text = report_analyzer.parse_file(temp_path)
        analysis = report_analyzer.analyze_report_text(raw_text)
        
        report_id = str(uuid.uuid4())
        memory_mgr.add_report(
            report_id=report_id, patient_id=patient_id, 
            summary=analysis.patient_explanation,
            report_type=analysis.report_type, report_date=analysis.report_date
        )
        
        if analysis.report_type == 'BreastCancer' and analysis.breast_data:
            memory_mgr.upsert_patient_profile(patient_id=patient_id, name=analysis.patient_name, diagnosis=analysis.breast_data.diagnosis)
            kg_updater.update_from_breast_cancer(patient_id, analysis.breast_data)
        elif analysis.report_type == 'ProstateCancer' and analysis.prostate_data:
            memory_mgr.upsert_patient_profile(patient_id=patient_id, name=analysis.patient_name, diagnosis=analysis.prostate_data.diagnosis)
            kg_updater.update_from_prostate_cancer(patient_id, analysis.prostate_data)
            
        memory_mgr.add_message(patient_id, "user", f"Uploaded medical report: {file.filename}")
        memory_mgr.add_message(patient_id, "assistant", f"Report analyzed. {analysis.patient_explanation}")

        return {"status": "success", "explanation": analysis.patient_explanation}
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/chat")
async def chat(req: ChatRequest):
    if not memory_mgr.get_patient_context(req.patient_id):
        raise HTTPException(status_code=404, detail="Patient not found.")

    # 1. Core Pipeline (Safety -> Context -> Retrieve -> LLM -> Save)
    result = pipeline.answer(req.query, patient_id=req.patient_id)
    
    if not result["safety"].get("allowed"):
        return {"answer": result["answer"], "safety": result["safety"]}

    answer = result["answer"]
    
    # 2. Citations Formatting
    # The pipeline currently returns raw dicts for sources. We reconstruct dummy Documents to use CitationManager.
    from langchain_core.documents import Document
    mock_docs = [Document(page_content="", metadata={"source": s["source"], "page": s["page"]}) for s in result["sources"]]
    citations = citation_manager.format_citations(mock_docs)
    
    # Append structured text citation to answer
    full_answer = f"{answer}\n\n{citations['formatted_text']}"

    # 3. Metrics (Mock scores for demonstration since core pipeline hides logits)
    conf_score = confidence_scorer.calculate_confidence([0.8], [0.9])
    
    rag_kag_context = result["knowledge_graph"] + "\n" + "\n".join([f"{s['source']}" for s in result["sources"]])
    is_grounded = hallucination_checker.is_grounded(answer, rag_kag_context)
    
    return {
        "answer": full_answer,
        "confidence": conf_score,
        "is_grounded": is_grounded,
        "knowledge_graph": result["knowledge_graph"],
        "citations": citations["structured"]
    }


# --- Interactive CLI Mode ---

def cli_mode():
    print("\n" + "="*50)
    print("Welcome to MedBot CLI")
    print("="*50)
    
    patient_id = input("Enter Patient ID (e.g. pat_001): ").strip()
    profile = memory_mgr.get_patient_context(patient_id)
    
    if not profile:
        print("\nNew patient detected. Please set up the profile.")
        name = input("Name: ")
        age = int(input("Age: "))
        gender = input("Gender: ")
        diagnosis = input("Primary Diagnosis: ")
        memory_mgr.upsert_patient_profile(
            patient_id=patient_id, name=name, age=age, gender=gender, diagnosis=diagnosis
        )
        print("Profile created successfully!\n")
    else:
        print(f"\nWelcome back, {profile['name']}!")
    
    while True:
        print("\nOptions:")
        print("1. Chat with MedBot")
        print("2. Upload Medical Report (Simulated via local path)")
        print("3. View Patient History")
        print("4. Exit")
        choice = input("\nSelect an option: ").strip()
        
        if choice == "1":
            while True:
                q = input(f"\n[{patient_id}] You: ").strip()
                if q.lower() in ["exit", "quit", "back"]:
                    break
                
                res = pipeline.answer(q, patient_id)
                print(f"\nMedBot: {res['answer']}")
                
                if res['safety'].get("allowed"):
                    mock_docs = [Document(page_content="", metadata={"source": s["source"], "page": s["page"]}) for s in res["sources"]]
                    cits = citation_manager.format_citations(mock_docs)
                    print(f"\n{cits['formatted_text']}")
                    
        elif choice == "2":
            path = input("Enter path to PDF/Image report: ").strip()
            if os.path.exists(path):
                raw = report_analyzer.parse_file(path)
                analysis = report_analyzer.analyze_report_text(raw)
                print(f"\nAnalysis Complete:\n{analysis.patient_explanation}")
                memory_mgr.add_message(patient_id, "assistant", f"Report analyzed. {analysis.patient_explanation}")
            else:
                print("File not found.")
                
        elif choice == "3":
            history = memory_mgr.get_recent_history(patient_id, limit=5)
            print("\n--- Recent History ---")
            for msg in history:
                print(f"[{msg['timestamp']}] {msg['role'].capitalize()}: {msg['content']}")
                
        elif choice == "4":
            print("Exiting MedBot. Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    import sys
    # If a command line arg is passed (like run server), we can hook uvicorn. 
    # By default, we launch the CLI to satisfy 'python main.py'
    if len(sys.argv) > 1 and sys.argv[1] == "server":
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    else:
        from langchain_core.documents import Document # Needed for CLI
        cli_mode()
