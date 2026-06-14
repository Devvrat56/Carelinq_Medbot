import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List

class PatientMemoryManager:
    def __init__(self, db_path: str = "medbot_patients.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Initializes tables for patient profiles, chat history, and reports."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 1. Patient Profiles
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    patient_id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    diagnosis TEXT,
                    psa_level REAL,
                    gleason_score TEXT,
                    current_treatment TEXT,
                    allergies TEXT,
                    updated_at TEXT NOT NULL
                )
            """)
            # 2. Conversation History
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    message TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            # 3. Reports
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    report_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    report_type TEXT,
                    report_date TEXT NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            conn.commit()

    def upsert_patient_profile(self, patient_id: str, name: str, age: int = None, 
                               gender: str = None, diagnosis: str = None, 
                               psa_level: float = None, gleason_score: str = None,
                               current_treatment: str = None, allergies: str = None):
        """Creates or updates a clinical patient profile."""
        now = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO patients (patient_id, name, age, gender, diagnosis, psa_level, 
                                      gleason_score, current_treatment, allergies, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(patient_id) DO UPDATE SET
                    name=excluded.name,
                    age=excluded.age,
                    gender=excluded.gender,
                    diagnosis=excluded.diagnosis,
                    psa_level=excluded.psa_level,
                    gleason_score=excluded.gleason_score,
                    current_treatment=excluded.current_treatment,
                    allergies=excluded.allergies,
                    updated_at=excluded.updated_at
            """, (patient_id, name, age, gender, diagnosis, psa_level, gleason_score, 
                  current_treatment, allergies, now))
            conn.commit()

    def get_patient_context(self, patient_id: str) -> Dict[str, Any]:
        """Retrieves structured clinical background metadata for system prompts."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
            row = cursor.fetchone()
            if not row:
                return {}
            return dict(row)

    def add_message(self, patient_id: str, role: str, message: str):
        """Appends a new turn to the patient's conversation history."""
        now = datetime.utcnow().isoformat()
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_history (patient_id, role, message, timestamp)
                VALUES (?, ?, ?, ?)
            """, (patient_id, role, message, now))
            conn.commit()

    def get_recent_history(self, patient_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetches recent chat history formatted for LLM ingestion."""
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            # limit represents pairs (turns), so multiply by 2 to get individual messages
            cursor.execute("""
                SELECT role, message, timestamp FROM chat_history 
                WHERE patient_id = ? 
                ORDER BY timestamp DESC LIMIT ?
            """, (patient_id, limit * 2))
            rows = cursor.fetchall()
            # Reverse list to maintain correct historical chronological order
            return [{"role": row["role"], "content": row["message"], "timestamp": row["timestamp"]} for row in reversed(rows)]

    def add_report(self, report_id: str, patient_id: str, summary: str, report_type: str, report_date: str):
        """Adds a processed report summary to the patient's record."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reports (report_id, patient_id, summary, report_type, report_date)
                VALUES (?, ?, ?, ?, ?)
            """, (report_id, patient_id, summary, report_type, report_date))
            conn.commit()
