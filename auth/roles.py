from enum import Enum

class Role(str, Enum):
    PATIENT = "PATIENT"
    DOCTOR = "DOCTOR"
    ADMIN = "ADMIN"
    RESEARCHER = "RESEARCHER"
