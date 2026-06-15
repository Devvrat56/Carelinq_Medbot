import sqlite3
import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PatientMemoryManager:
    def __init__(self, db_path: str = "medbot_patients.db"):
        self.db_path = db_path
        
        # Load credentials
        self.postgres_url = os.getenv("POSTGRES_URL")
        self.mongo_uri = os.getenv("MONGO_URI")
        
        self.pg_conn = None
        self.mongo_client = None
        self.mongo_db = None
        self.chat_collection = None
        
        self._init_connections()

    def _init_connections(self):
        """Initializes database connections (Postgres/Mongo) with SQLite fallback."""
        # 1. Try PostgreSQL
        if self.postgres_url:
            try:
                import psycopg2
                from psycopg2.extras import RealDictCursor
                self.pg_conn = psycopg2.connect(self.postgres_url)
                logger.info("Connected to PostgreSQL for structured data.")
                self._init_postgres()
            except Exception as e:
                logger.warning(f"Failed to connect to PostgreSQL: {e}. Falling back to SQLite.")
                self.pg_conn = None

        # 2. Try MongoDB
        if self.mongo_uri:
            try:
                from pymongo import MongoClient
                self.mongo_client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
                # Verify connection
                self.mongo_client.server_info()
                self.mongo_db = self.mongo_client["medbot"]
                self.chat_collection = self.mongo_db["chat_history"]
                # Create indexes
                self.chat_collection.create_index("patient_id")
                self.chat_collection.create_index("timestamp")
                logger.info("Connected to MongoDB for chat history.")
            except Exception as e:
                logger.warning(f"Failed to connect to MongoDB: {e}. Falling back to SQLite for chat history.")
                self.mongo_client = None
                
        # 3. Always initialize SQLite as the baseline fallback
        self._init_sqlite()

    def _get_sqlite_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_postgres(self):
        with self.pg_conn.cursor() as cursor:
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
                    updated_at TIMESTAMP NOT NULL
                )
            """)
            # 3. Reports
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    report_id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    report_type TEXT,
                    report_date TIMESTAMP NOT NULL,
                    FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
                )
            """)
            self.pg_conn.commit()

    def _init_sqlite(self):
        """Initializes local SQLite tables for patient profiles, chat history, and reports."""
        with self._get_sqlite_connection() as conn:
            cursor = conn.cursor()
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
        
        if self.pg_conn:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO patients (patient_id, name, age, gender, diagnosis, psa_level, 
                                          gleason_score, current_treatment, allergies, updated_at)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT(patient_id) DO UPDATE SET
                        name=EXCLUDED.name,
                        age=EXCLUDED.age,
                        gender=EXCLUDED.gender,
                        diagnosis=EXCLUDED.diagnosis,
                        psa_level=EXCLUDED.psa_level,
                        gleason_score=EXCLUDED.gleason_score,
                        current_treatment=EXCLUDED.current_treatment,
                        allergies=EXCLUDED.allergies,
                        updated_at=EXCLUDED.updated_at
                """, (patient_id, name, age, gender, diagnosis, psa_level, gleason_score, 
                      current_treatment, allergies, now))
                self.pg_conn.commit()
        else:
            with self._get_sqlite_connection() as conn:
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
        if self.pg_conn:
            from psycopg2.extras import RealDictCursor
            with self.pg_conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute("SELECT * FROM patients WHERE patient_id = %s", (patient_id,))
                row = cursor.fetchone()
                if not row:
                    return {}
                return dict(row)
        else:
            with self._get_sqlite_connection() as conn:
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
        
        if self.mongo_client:
            doc = {
                "patient_id": patient_id,
                "role": role,
                "message": message,
                "timestamp": now
            }
            self.chat_collection.insert_one(doc)
        else:
            with self._get_sqlite_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO chat_history (patient_id, role, message, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (patient_id, role, message, now))
                conn.commit()

    def get_recent_history(self, patient_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetches recent chat history formatted for LLM ingestion."""
        # limit represents pairs (turns), so multiply by 2 to get individual messages
        fetch_limit = limit * 2
        
        if self.mongo_client:
            cursor = self.chat_collection.find(
                {"patient_id": patient_id},
                {"_id": 0, "role": 1, "message": 1, "timestamp": 1}
            ).sort("timestamp", -1).limit(fetch_limit)
            
            rows = list(cursor)
            return [{"role": row["role"], "content": row["message"], "timestamp": row["timestamp"]} for row in reversed(rows)]
        else:
            with self._get_sqlite_connection() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT role, message, timestamp FROM chat_history 
                    WHERE patient_id = ? 
                    ORDER BY timestamp DESC LIMIT ?
                """, (patient_id, fetch_limit))
                rows = cursor.fetchall()
                return [{"role": row["role"], "content": row["message"], "timestamp": row["timestamp"]} for row in reversed(rows)]

    def add_report(self, report_id: str, patient_id: str, summary: str, report_type: str, report_date: str):
        """Adds a processed report summary to the patient's record."""
        if self.pg_conn:
            with self.pg_conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO reports (report_id, patient_id, summary, report_type, report_date)
                    VALUES (%s, %s, %s, %s, %s)
                """, (report_id, patient_id, summary, report_type, report_date))
                self.pg_conn.commit()
        else:
            with self._get_sqlite_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO reports (report_id, patient_id, summary, report_type, report_date)
                    VALUES (?, ?, ?, ?, ?)
                """, (report_id, patient_id, summary, report_type, report_date))
                conn.commit()
