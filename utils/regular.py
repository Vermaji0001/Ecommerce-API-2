from passlib.context import CryptContext
from sqlalchemy.orm import Session
from modals.all_modals import Coustomer,Manufacturer
from fastapi import HTTPException
from typing import Optional
from datetime import timedelta,datetime
from env.private_data import EXPIRY_MINUTES,SECRET_KEY,ALGORITHM
from jose import jwt


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


def craete_token(data:dict,expire:Optional[timedelta]=None):
    new_data=data.copy()
    if expire:
        expire=datetime.now()+expire
    else:
        expire=datetime.now()+timedelta(minutes=EXPIRY_MINUTES)
    new_data.update({"exp":expire})
    token=jwt.encode(new_data,SECRET_KEY,ALGORITHM)
    return token
