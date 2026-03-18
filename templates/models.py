from pydantic import BaseModel

class LoginRequest(BaseModel):
    id: str
    password: str
    
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int