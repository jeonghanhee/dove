import uuid
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class LoginRequest(BaseModel):
    id: str
    password: str

USER_DATA = {
    "superadmin": "12345678@1"
}

@app.post("/login")
async def login(request: LoginRequest):
    stored_password = USER_DATA.get(request.id)
    
    if stored_password and stored_password == request.password:
        access_token = f"access_{uuid.uuid4().hex}"
        refresh_token = f"refresh_{uuid.uuid4().hex}"
        
        print(f"[{datetime.now()}] Login Success: {request.id}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": 3600
        }
    
    print(f"[{datetime.now()}] Login Failed: {request.id}")
    raise HTTPException(status_code=401, detail="Invalid ID or Password")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)