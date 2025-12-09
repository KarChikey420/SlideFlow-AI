from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker,declarative_base
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL,pool_pre_ping=True)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

class User(Base):
    __tablename__="users1"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(255),nullable=False)
    email=Column(String(255),unique=True,nullable=False)
    password=Column(String(255),nullable=False)
    
Base.metadata.create_all(bind=engine)

    