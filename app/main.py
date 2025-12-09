from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
import bcrypt
import uuid 
import os
from backend.database import SessionLocal,User
from backend.auth import create_access_token,current_user
from ppt_content.generator import create_presentation
from ppt_content.pptx_file import create_ppt
import uvicorn

app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "https://slideflow-ai.onrender.com",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    )
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class GeneratePPTRequest(BaseModel):
    topic: str
    slide: int = 10

@app.options("/{path:path}")
def options_handler(path: str):
    return {"message": "OK"}

@app.post("/signup")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user:
        raise HTTPException(400, "User already exists")

    hashed = hash_password(request.password)
    new_user = User(name=request.name, email=request.email, password=hashed)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}


@app.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    if not verify_password(request.password, user.password):
        raise HTTPException(401, "Wrong password")

    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/generate_pptx")
def generate_pptx(request: GeneratePPTRequest, current_user:str= Depends(current_user)):
    slides=create_presentation(request.topic,request.slide)
    safe_topic = "".join(c for c in request.topic if c.isalnum() or c in (' ', '_')).replace(' ','_')
    filename=f"{safe_topic}_{uuid.uuid4().hex}.pptx"
    create_ppt(slides,filename,request.topic)
    
    try:
        return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=filename)
    finally:
        if os.path.exists(filename):
            os.remove(filename)
        
        
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)