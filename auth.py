from datetime import datetime,timedelta
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from starlette import status
from sqlalchemy.orm   import Session
from config import session
from dbmodels import Userdb
import dbmodels
from  passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import jwt,JWTError
import os
from config import get_db
from fastapi import FastAPI ,Depends

router=APIRouter()

app=FastAPI()
class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = os.getenv("ALGORITHM")
    EXPIRY_TIME = int(os.getenv("EXPIRY_TIME", 15))

settings = Settings()

def create_token(username:str):
    expire = datetime.utcnow() + timedelta(minutes=settings.EXPIRY_TIME)
    payload = {"sub": username,
    "exp": expire,
    "iat": datetime.utcnow()}
    token = jwt.encode(payload,settings.SECRET_KEY,settings.ALGORITHM)
    return token
 
 


@router.post("/register")
def register(username:str,passwd:str,db:Session=Depends(get_db)):
    db_users = db.query(dbmodels.Userdb).filter(dbmodels.Userdb.username==username).first()
    if(db_users):
        return "userAlready Exists"
    else:
        db.add(dbmodels.Userdb(username=username,password=passwd))
        db.commit()
        return {"message": "User created"}
    
@router.post("/login")
def login(username:str ,passwd:str,db:Session=Depends(get_db)):
    db_users = db.query(dbmodels.Userdb).filter(dbmodels.Userdb.username==username).first()
    if db_users is None:
        raise HTTPException(status_code=404, detail="User not found")
    if(db_users.password==passwd):
        return create_token(username)
    return {"message":"password mismatch or User Not found"}