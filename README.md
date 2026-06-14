# Medical Chatbot App

A sophisticated Retrieval-Augmented Generation (RAG) chatbot designed specifically for the medical domain. This system enables intelligent parsing of medical records, robust tracking of patient profiles, and context-aware clinical reasoning.

## 🚀 Features

- **Medical Document Parsing (`report_analyzer.py`)**: 
  - Extracts text natively from medical PDFs.
  - Automatically falls back to OCR (`pytesseract`, `pdf2image`) for scanned images or faxes.
  - Generates patient-friendly explanations from complex clinical terms and biomarkers using Structured LLM output.
- **RAG Engine (`rag_pipeline.py`, `retrieve.py`, `reranker.py`)**:
  - Employs a fully featured Retrieval-Augmented Generation pipeline.
  - Vector retrieval capabilities through ChromaDB.
  - Context re-ranking mechanism to bubble up the most relevant medical guidelines or past history.
- **Patient Memory Management (`memory.py`)**:
  - Leverages SQLite databases (`clinic_test.db`, `temp_db`) to store conversational context persistently.
  - Maintains detailed patient profiles including demographics, prior conditions, and known allergies.
- **Data Extraction & Prompt Management**:
  - Custom system and chain-of-thought prompts configured explicitly for clinical settings (`prompt.py`).
  - Automated configurations via `.env` files and `config.py`.

## 🛠️ Requirements & Setup

This project utilizes `langchain`, `pypdf`, `pytesseract`, and `langchain-openai`. To set up your local environment:

1. **Install Python Dependencies:**
   ```bash
   pip install pypdf pytesseract pdf2image langchain-openai
   # Also ensure you install dependencies required by your specific RAG/Retrieval setup (e.g. chromadb, sentence-transformers, etc.)
   ```

2. **System Dependencies:**
   - **Tesseract OCR**: Required for parsing image-based PDFs. 
     - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
     - Mac/Homebrew: `brew install tesseract`
   - **Poppler**: Required for `pdf2image` to rasterize PDFs.
     - Ubuntu/Debian: `sudo apt-get install poppler-utils`
     - Mac/Homebrew: `brew install poppler`

3. **Environment Variables:**
   Create a `.env` file at the root of `Chatbot_app` with your necessary API keys:
   ```env
   OPENAI_API_KEY="your-openai-api-key"
   GROQ_API_KEY="your-groq-api-key" # If utilizing Groq models
   ```

## 🏗️ Project Structure

```
Chatbot_app/
├── .env                    # Secret API keys and environment variables
├── chroma_db/              # Persistent vector store database
├── temp_db/                # Temporary/cache databases (like SQLite memory)
├── Data_extraction/        # Raw data handling and preprocessing scripts
└── retriever/              # Core logic for the Chatbot
    ├── config.py           # Configuration variables and loaders
    ├── memory.py           # SQLite-based Patient Profile and Chat History manager
    ├── prompt.py           # Core System Prompts and Chain-of-Thought templates
    ├── rag_pipeline.py     # Main RAG orchestration logic
    ├── report_analyzer.py  # OCR and Medical Report structured parsing
    ├── reranker.py         # Advanced document re-ranking
    └── retrieve.py         # Core Vector Database retrieval operations
```

## 🧠 Usage

1. **Upload & Analyze a Report:**
   The `report_analyzer.py` contains a runner that showcases how to analyze an uploaded `sample_lab_result.pdf`. It will register a dummy patient, perform OCR/text extraction, and save a patient-friendly LLM explanation to the SQL memory.
   
   ```bash
   cd retriever
   python report_analyzer.py
   ```

2. **Engaging the Chatbot:**
   You can instantiate the `rag_pipeline.py` or the main runner to interact directly with patient histories and the Vector DB.
