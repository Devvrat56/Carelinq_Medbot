import streamlit as st
import requests
import json

st.set_page_config(page_title="MedBot Consultation", page_icon="🩺", layout="wide")

API_BASE_URL = "http://localhost:8000"

st.title("🩺 MedBot Clinical Assistant")
st.markdown("Your intelligent medical consultation system powered by RAG and Knowledge Graphs.")

# Sidebar for Patient Management
with st.sidebar:
    st.header("Patient Profile")
    patient_id = st.text_input("Patient ID (e.g. pat_123)", value="pat_001")
    
    st.divider()
    st.header("Upload Clinical Report")
    uploaded_file = st.file_uploader("Upload PDF or Image", type=["pdf", "png", "jpg", "jpeg"])
    if uploaded_file and st.button("Analyze Report"):
        with st.spinner("Analyzing report..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            data = {"patient_id": patient_id}
            try:
                response = requests.post(f"{API_BASE_URL}/upload-report", files=files, data=data)
                if response.status_code == 200:
                    result = response.json()
                    st.success("Report Analyzed Successfully!")
                    with st.expander("View Extraction Details"):
                        st.json(result)
                else:
                    st.error(f"Failed to analyze report: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Fetch history if changed
if "current_patient" not in st.session_state or st.session_state.current_patient != patient_id:
    st.session_state.current_patient = patient_id
    try:
        resp = requests.get(f"{API_BASE_URL}/patient/{patient_id}")
        if resp.status_code == 200:
            profile = resp.json()
            history = profile.get("chat_history", [])
            st.session_state.messages = []
            for h in history:
                if h["role"] == "user":
                    st.session_state.messages.append({"role": "user", "content": h["content"]})
                else:
                    st.session_state.messages.append({"role": "assistant", "content": h["content"]})
    except:
        st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask a medical question..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call Backend
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        with st.spinner("Consulting knowledge base..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat",
                    json={"query": prompt, "patient_id": patient_id}
                )
                if response.status_code == 200:
                    data = response.json()
                    answer = data.get("answer", "")
                    
                    # Formatting Metrics
                    metrics = data.get("metrics", {})
                    confidence = metrics.get("confidence_score", 0.0)
                    safety = metrics.get("safety_status", "unknown")
                    hallucination = metrics.get("hallucination_flag", False)
                    citations = data.get("formatted_citations", "")

                    formatted_response = f"{answer}\n\n"
                    formatted_response += "---\n"
                    formatted_response += f"**Confidence:** `{confidence:.2f}` | **Safety:** `{safety}` | **Grounded:** `{'❌ No' if hallucination else '✅ Yes'}`\n\n"
                    
                    if citations:
                        formatted_response += f"**Sources:**\n{citations}"

                    message_placeholder.markdown(formatted_response)
                    st.session_state.messages.append({"role": "assistant", "content": formatted_response})
                else:
                    error_msg = f"Error: {response.text}"
                    message_placeholder.error(error_msg)
            except Exception as e:
                message_placeholder.error(f"Failed to connect to backend: {e}")
