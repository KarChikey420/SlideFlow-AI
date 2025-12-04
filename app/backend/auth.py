from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends,HTTPException,status
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY=os.getenv("Secret_key")
ALGORITHM=os.getenv("Algorithm")
oath2_scheme=OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(minutes=30)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)

def current_user(token:str=Depends(oath2_scheme)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(401,"Invalid Token")
    