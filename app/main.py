from fastapi import FastAPI,Depends,HTTPException
from fastapi.responses import FileResponse
from passlib.context import CryptContext
import uuid 
from app.backend.database import SessionLocal,User
from app.backend.auth import create_access_token,current_user
from app.ppt_content.generator import create_presentation
from app.ppt_content.pptx_file import create_ppt
import uvicorn

app=FastAPI()

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

@app.post("/signup")
def signup(name:str,email:str,password:str):
    db=SessionLocal()
    if db.query(User).filter(User.email==email).first():
        raise HTTPException(400,"User already exists")
    
    hashed=pwd_context.hash(password)
    user=User(name=name, email=email, password=hashed)
    db.add(user)
    db.commit()
    return {"message":"User created successfully"}

@app.post("/login")
def login(email:str,password:str):
    db=SessionLocal()
    
    user=db.query(User).filter(User.email==email).first()
    if not user:
        raise HTTPException(404, "User not found")
    if not pwd_context.verify(password,user.password):
        raise HTTPException(401,"Wrong password")
    token=create_access_token({"sub":user.email})
    return {"access_token":token, "token_type":"bearer"}

@app.post("/generate_ppx")
def generate_pptx(topic:str,slide:int=10,current_user:str= Depends(current_user)):
    slides=create_presentation(topic,slide)
    filename=f"{topic.replace('','_')}_{uuid.uuid4().hex}.pptx"
    create_ppt(slides,filename)
    
    return FileResponse(filename, media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation", filename=filename)
        
        
if __name__=="__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    