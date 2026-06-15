from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from auth.jwt_handler import create_access_token
from auth.roles import Role

router = APIRouter(prefix="/auth", tags=["auth"])

# Dummy database of users for demonstration purposes
USERS_DB = {
    "patient1": {"password": "password123", "role": Role.PATIENT},
    "dr_smith": {"password": "password123", "role": Role.DOCTOR},
    "admin_joe": {"password": "password123", "role": Role.ADMIN},
}

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(req: LoginRequest):
    user = USERS_DB.get(req.username)
    if not user or user["password"] != req.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_access_token(data={"sub": req.username, "role": user["role"].value})
    return {"access_token": token, "token_type": "bearer"}
