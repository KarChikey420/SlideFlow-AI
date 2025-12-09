from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import hashlib
import uuid 
from backend.database import SessionLocal,User
from backend.auth import create_access_token,current_user
from ppt_content.generator import create_presentation
from ppt_content.pptx_file import create_ppt
import uvicorn

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hashlib.sha256(password.encode()).hexdigest() == hashed

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

@app.post("/generate_ppx")
def generate_pptx(request: GeneratePPTRequest, current_user:str= Depends(current_user)):
    slides=create_presentation(request.topic,request.slide)
    filename=f"{request.topic.replace(' ','_')}_{uuid.uuid4().hex}.pptx"
    create_ppt(slides,filename,request.topic)
    
    return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=filename)
        
        
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    