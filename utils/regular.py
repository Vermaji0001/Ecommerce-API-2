from passlib.context import CryptContext
from sqlalchemy.orm import Session
from modals.all_modals import Coustomer,Manufacturer
from fastapi import HTTPException,Depends
from typing import Optional
from datetime import timedelta,datetime
from env.private_data import EXPIRY_MINUTES,SECRET_KEY,ALGORITHM
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from utils.maindata import get_db


oauth2_scheme=OAuth2PasswordBearer(tokenUrl="logintoken")


passwordxyz=CryptContext(schemes=["argon2"])
def password_hash(data):
    return passwordxyz.hash(data)


def varify_password(orginal_password:str,hash_password:str):
    return passwordxyz.verify(orginal_password,hash_password)


def coustomer_authentication(email,password,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==email).first()
    if not coustomer:
        raise HTTPException (status_code=404,detail="not match your email")
    new_password=varify_password(password,coustomer.password)
    if not new_password:
        raise HTTPException(status_code=404,detail="not match your password")
    return coustomer



def manufacturer_authentication(email,password,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==email).first()
    if not manufacturer:
        raise HTTPException (status_code=404,detail="not match your email")
    new_password=varify_password(password,manufacturer.password)
    if not new_password:
        raise HTTPException(status_code=404,detail="not match your password")
    return manufacturer


def create_token(data:dict,expire:Optional[timedelta]=None):
    new_data=data.copy()
    if expire:
        expire=datetime.now()+expire
    else:
        expire=datetime.now()+timedelta(minutes=EXPIRY_MINUTES)
    new_data.update({"exp":expire})
    token=jwt.encode(new_data,SECRET_KEY,ALGORITHM)
    return token

def coustomer_data_by_token(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
       
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        coustomer_id=payload.get("sub")
        
        if coustomer_id is None:
           raise HTTPException (status_code=404,detail="Not found  id data")
    except JWTError:
            raise HTTPException (status_code=404,detail="JWT error plaese check ")
    coustomer=db.query(Coustomer).filter(Coustomer.id==int(coustomer_id)).first()
    if not coustomer:
        raise HTTPException (status_code=404,detail="Not match your token id ")
    return coustomer




#get manufacturer data by token
def manufacturer_data_by_token(token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        
        manufacturer_id=payload.get("sub")
        
        if manufacturer_id is None:
           raise HTTPException (status_code=404,detail="Not found  id data")
    except JWTError:
            raise HTTPException (status_code=404,detail="JWT error plaese check ")
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==int(manufacturer_id)).first()
    if not manufacturer:
        raise HTTPException (status_code=404,detail="Not match your token id ")
    return manufacturer

