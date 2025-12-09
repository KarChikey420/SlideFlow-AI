from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "test.db")

DATABASE_URL = f"sqlite:///{DB_PATH}"
engine=create_engine(DATABASE_URL,connect_args={"check_same_thread":False})
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50))
    email=Column(String(50))
    password=Column(String(50))
    
Base.metadata.create_all(bind=engine)

    