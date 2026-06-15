import streamlit as st
import os
import sys
import uuid
import logging
import tempfile

# Add the root project directory to sys.path so we can import internal modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Internal MedBot Modules
from Data_safety.confidence import ConfidenceScorer
from Data_safety.hallucination_checker import HallucinationChecker
from retriever.citation_manager import CitationManager
from retriever.memory import PatientMemoryManager
from retriever.report_analyzer import MedicalReportAnalyzer
from retriever.kag_rag_pipeline import KAGRAGPipeline
from knowledge_graph.kg_updater import KnowledgeGraphUpdater
from storage.blob_manager import BlobManager
from langchain_core.documents import Document

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

st.set_page_config(page_title="MedBot Consultation", page_icon="🩺", layout="wide")

@st.cache_resource
def init_services():
    logging.info("Initializing MedBot backend services in Streamlit...")
    return {
        "memory_mgr": PatientMemoryManager("medbot_patients.db"),
        "pipeline": KAGRAGPipeline(),
        "confidence_scorer": ConfidenceScorer(),
        "hallucination_checker": HallucinationChecker(),
        "citation_manager": CitationManager(),
        "report_analyzer": MedicalReportAnalyzer(),
        "kg_updater": KnowledgeGraphUpdater(),
        "blob_manager": BlobManager()
    }

services = init_services()

st.title("🩺 MedBot Clinical Assistant")
st.markdown("Your intelligent medical consultation system powered by RAG and Knowledge Graphs.")

# Sidebar for Patient Management
with st.sidebar:
    st.header("Patient Profile")
    patient_id = st.text_input("Patient ID (e.g. pat_123)", value="pat_001")
    
    # Ensure patient profile exists
    if not services["memory_mgr"].get_patient_context(patient_id):
        if st.button("Create Profile for this ID"):
            services["memory_mgr"].upsert_patient_profile(
                patient_id=patient_id, name="Test Patient", age=0, gender="Unknown", diagnosis="None"
            )
            st.success(f"Profile {patient_id} created!")
            st.rerun()
        else:
            st.warning(f"Patient {patient_id} does not exist. Please create the profile first.")

    st.divider()
    st.header("Upload Clinical Report")
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file and st.button("Analyze Report"):
        if not services["memory_mgr"].get_patient_context(patient_id):
            st.error("Patient not found. Create patient first.")
        else:
            with st.spinner("Analyzing report..."):
                try:
                    # Upload to Azure Blob Storage (if available)
                    file_bytes = uploaded_file.getvalue()
                    try:
                        services["blob_manager"].upload_report(uploaded_file.name, file_bytes)
                    except Exception as e:
                        logging.warning(f"Failed to upload to Azure Blob Storage: {e}")

                    # Write to temp file for local processing
                    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}") as temp_file:
                        temp_file.write(file_bytes)
                        temp_path = temp_file.name
                        
                    # Process report
                    raw_text = services["report_analyzer"].parse_file(temp_path)
                    analysis = services["report_analyzer"].analyze_report_text(raw_text)
                    
                    report_id = str(uuid.uuid4())
                    services["memory_mgr"].add_report(
                        report_id=report_id, patient_id=patient_id, 
                        summary=analysis.patient_explanation,
                        report_type=analysis.report_type, report_date=analysis.report_date
                    )
                    
                    if analysis.report_type == 'BreastCancer' and analysis.breast_data:
                        services["memory_mgr"].upsert_patient_profile(patient_id=patient_id, name=analysis.patient_name, diagnosis=analysis.breast_data.diagnosis)
                        services["kg_updater"].update_from_breast_cancer(patient_id, analysis.breast_data)
                    elif analysis.report_type == 'ProstateCancer' and analysis.prostate_data:
                        services["memory_mgr"].upsert_patient_profile(patient_id=patient_id, name=analysis.patient_name, diagnosis=analysis.prostate_data.diagnosis)
                        services["kg_updater"].update_from_prostate_cancer(patient_id, analysis.prostate_data)
                        
                    services["memory_mgr"].add_message(patient_id, "user", f"Uploaded medical report: {uploaded_file.name}")
                    services["memory_mgr"].add_message(patient_id, "assistant", f"Report analyzed. {analysis.patient_explanation}")

                    st.success("Report Analyzed Successfully!")
                    with st.expander("Patient Explanation"):
                        st.write(analysis.patient_explanation)

                    # Cleanup temp file
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

                except Exception as e:
                    st.error(f"Failed to analyze report: {e}")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fetch history if changed
if "current_patient" not in st.session_state or st.session_state.current_patient != patient_id:
    st.session_state.current_patient = patient_id
    profile = services["memory_mgr"].get_patient_context(patient_id)
    if profile:
        history = services["memory_mgr"].get_recent_history(patient_id, limit=10)
        st.session_state.messages = []
        for h in history:
            st.session_state.messages.append({"role": h["role"], "content": h["content"]})
    else:
        st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a medical question..."):
    if not services["memory_mgr"].get_patient_context(patient_id):
        st.error(f"Please create the patient profile for {patient_id} first.")
    else:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Call Backend Pipeline Directly
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("Consulting knowledge base..."):
                try:
                    result = services["pipeline"].answer(prompt, patient_id=patient_id)
                    
                    if not result["safety"].get("allowed"):
                        answer = result["answer"]
                        safety_status = "Blocked"
                        confidence = 0.0
                        hallucination = False
                        formatted_response = answer
                    else:
                        answer = result["answer"]
                        
                        # Mock Document format for citation manager
                        mock_docs = [Document(page_content="", metadata={"source": s["source"], "page": s["page"]}) for s in result["sources"]]
                        citations = services["citation_manager"].format_citations(mock_docs)
                        
                        conf_score = services["confidence_scorer"].calculate_confidence([0.8], [0.9])
                        rag_kag_context = result["knowledge_graph"] + "\n" + "\n".join([f"{s['source']}" for s in result["sources"]])
                        is_grounded = services["hallucination_checker"].is_grounded(answer, rag_kag_context)

                        confidence = conf_score
                        safety_status = result["safety"].get("category", "Safe")
                        hallucination = not is_grounded
                        
                        formatted_response = f"{answer}\n\n"
                        formatted_response += "---\n"
                        formatted_response += f"**Confidence:** `{confidence:.2f}` | **Safety:** `{safety_status}` | **Grounded:** `{'❌ No' if hallucination else '✅ Yes'}`\n\n"
                        
                        if citations.get("formatted_text"):
                            formatted_response += f"**Sources:**\n{citations['formatted_text']}"

                    message_placeholder.markdown(formatted_response)
                    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                    
                except Exception as e:
                    message_placeholder.error(f"Failed to process query: {e}")
