
from sqlalchemy.orm import Session
from modals.all_modals import Coustomer,Otp
from fastapi import HTTPException
from utils.regular import password_hash,varify_password

from utils.regular import coustomer_authentication
import random




#coustomer register
s=["@","#","$","&"]
def coustomer_register(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if coustomer:
        raise HTTPException (status_code=404,detail="your email is already exists")
    for i in s:
        if i in data.password:
           if len(data.password)>=8: 
              if data.dob:
                hash_password=password_hash(data.password)
                xyz=Coustomer(name=data.name,
                          email=data.email,
                          password=hash_password,
                          dob=data.dob,
                          referal_code=data.referal_code)
                db.add(xyz)
                db.commit()
                db.refresh(xyz)
                return {"coustomer is register"}
              raise HTTPException (status_code=404,detail="entre your dob")
           raise HTTPException(status_code=404,detail="your password length is lessthan 8 ")
    raise HTTPException (status_code=404,detail="use speacial crackter")



def coustomer_login(data,db:Session):
     verify=coustomer_authentication(data.email,data.password,db)
     if not verify:
         raise HTTPException(status_code=404,detail="invalid information")
     return {"msg":"login"}


s=["@","#","$","&"]
def change_password(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not match your id ")
    if varify_password(data.old_password,coustomer.password):
     for i in s:
        if i in data.new_password:
            if len(data.new_password)>=8:
                new_hash=password_hash(data.new_password)
                coustomer.password=new_hash
                db.commit()
                db.refresh(coustomer)
                return{"msg":"change your password"}
            raise HTTPException(status_code=404,detail="your length of passwod is less than 8")
     raise HTTPException(status_code=404,detail="use special crackter in password")
    raise HTTPException(status_code=404,detail="not match your old password")
    


def sent_opt(data,db:Session):
    
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not match your email")
    new_otp=random.randint(1111,9999)
    xyz=Otp(email=data.email,otp=new_otp)
    
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":f"sent otp this email {data.email},Otp {new_otp}"}


s=["@","#","$","&"]
def reset_password(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not match your email")
    coustomer=db.query(Otp).filter(Otp.email==data.email).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not sent otp this email")
    if coustomer.otp==data.otp:
        for i in s:
            if i in data.new_password:
                if len(data.new_password)>=8:
                   new_hash=password_hash(data.new_password)
                   coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
                   coustomer.password=new_hash
                   db.commit()
                   db.refresh(coustomer)
                   return {"msg":"reset your password"}
                raise HTTPException(status_code=404,detail="length of password is less than 8")
            raise HTTPException(status_code=404,detail="use special crackter in password")
    raise HTTPException(status_code=404,detail="not match your otp")
    
    
  
           