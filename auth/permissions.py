from fastapi import HTTPException, Security
from auth.jwt_handler import decode_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from auth.roles import Role

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

def require_roles(allowed_roles: List[Role]):
    def role_checker(credentials: HTTPAuthorizationCredentials = Security(security)):
        user = get_current_user(credentials)
        if user.get("role") not in [role.value for role in allowed_roles]:
            raise HTTPException(status_code=403, detail="Operation not permitted")
        return user
    return role_checker
