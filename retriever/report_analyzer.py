import os
import pypdf
from pdf2image import convert_from_path
import pytesseract
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional
from context3 import get_contextualized_report_system

# Define specific schemas
class ProstateCancerData(BaseModel):
    diagnosis: str = Field(description="The primary diagnosis")
    psa_level: str = Field(description="PSA level if mentioned")
    gleason_score: str = Field(description="Gleason score if mentioned")
    grade_group: str = Field(description="Grade group if mentioned")
    clinical_stage: str = Field(description="Clinical stage if mentioned")
    lymph_nodes: str = Field(description="Lymph node status if mentioned")
    current_treatment: str = Field(description="Current treatment if mentioned")

class BreastCancerData(BaseModel):
    diagnosis: str = Field(description="The primary diagnosis")
    er_status: str = Field(description="Estrogen Receptor status")
    pr_status: str = Field(description="Progesterone Receptor status")
    her2_status: str = Field(description="HER2 status")
    ki67: str = Field(description="Ki67 proliferation index")
    tumor_size: str = Field(description="Tumor size")
    stage: str = Field(description="Cancer stage")

class GeneralReportData(BaseModel):
    diagnosis: str = Field(description="Primary diagnosis or summary")
    extracted_entities: list[str] = Field(description="Key findings, biomarkers, abnormal vitals, or clinical terms.")

class UnifiedReportAnalysis(BaseModel):
    report_type: str = Field(description="Type of report: 'ProstateCancer', 'BreastCancer', or 'General'")
    patient_name: str = Field(description="Name of the patient if found, otherwise 'Unknown'")
    report_date: str = Field(description="Date the lab test or medical report was generated. You MUST format this strictly as YYYY-MM-DD (e.g. 2024-10-17).")
    
    # Only one of these will be fully populated based on report_type
    prostate_data: Optional[ProstateCancerData] = None
    breast_data: Optional[BreastCancerData] = None
    general_data: Optional[GeneralReportData] = None
    
    patient_explanation: str = Field(description="An empathetic, patient-friendly explanation in non-technical terms. Reassuring, clear, and highlights actionable next steps or things to discuss with their physician. Do not use alarming jargon.")

class MedicalReportAnalyzer:
    def __init__(self):
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.1, 
            api_key=os.getenv("GROQ_API_KEY"))
        self.structured_llm = llm.with_structured_output(UnifiedReportAnalysis)
        
    def _extract_native_text(self, pdf_path: str) -> str:
        text = ""
        try:
            with open(pdf_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            pass
        return text.strip()

    def _extract_ocr_text(self, pdf_path: str) -> str:
        text = ""
        try:
            pages = convert_from_path(pdf_path, dpi=200)
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"
        except Exception:
            pass
        return text.strip()

    def parse_file(self, file_path: str) -> str:
        """Extracts text using standard readers, cascading to OCR if empty or if it's an image."""
        ext = file_path.lower().split('.')[-1]
        
        if ext in ['png', 'jpg', 'jpeg']:
            import PIL.Image
            return pytesseract.image_to_string(PIL.Image.open(file_path)).strip()
        
        extracted_text = self._extract_native_text(file_path)
        if len(extracted_text) < 50:
            extracted_text = self._extract_ocr_text(file_path)
            
        return extracted_text

    def analyze_report_text(self, raw_text: str) -> UnifiedReportAnalysis:
        system_base = get_contextualized_report_system("full")
        sys_prompt = system_base + "\n\nCategorize the medical report into 'ProstateCancer', 'BreastCancer', or 'General'. Then populate the relevant data fields. Always generate a comforting patient_explanation summarizing the findings."
        prompt = ChatPromptTemplate.from_messages([
            ("system", sys_prompt),
            ("human", "Analyze the following raw clinical report text:\n\n{report_data}")
        ])
        chain = prompt | self.structured_llm
        return chain.invoke({"report_data": raw_text})

if __name__ == "__main__":
    from retriever.memory import PatientMemoryManager
    from knowledge_graph.kg_updater import KnowledgeGraphUpdater
    import uuid

    memory = PatientMemoryManager("medbot_patients.db")
    analyzer = MedicalReportAnalyzer()
    kg_updater = KnowledgeGraphUpdater()
    
    p_id = "pat_demo"
    memory.upsert_patient_profile(patient_id=p_id, name="Jane Doe", age=45, gender="Female")
    
    sample_text = "ER positive. PR positive. HER2 negative. Ki67: 15%. Diagnosis: Invasive ductal carcinoma."
    
    print("[1] Analyzing medical data via LLM...")
    try:
        analysis = analyzer.analyze_report_text(sample_text)
        
        report_id = str(uuid.uuid4())
        memory.add_report(
            report_id=report_id,
            patient_id=p_id,
            summary=analysis.patient_explanation,
            report_type=analysis.report_type,
            report_date=analysis.report_date
        )
        
        if analysis.report_type == 'BreastCancer' and analysis.breast_data:
            memory.upsert_patient_profile(
                patient_id=p_id,
                name=analysis.patient_name,
                diagnosis=analysis.breast_data.diagnosis
            )
            kg_updater.update_from_breast_cancer(p_id, analysis.breast_data)

        print("\n--- PATIENT EXPLANATION OUTPUT ---")
        print(analysis.patient_explanation)
    except Exception as e:
        print(f"Error during analysis: {e}. Please ensure API keys are set correctly.")
