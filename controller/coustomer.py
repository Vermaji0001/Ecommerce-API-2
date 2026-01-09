
from sqlalchemy.orm import Session
from modals.all_modals import Coustomer,Otp,Product,Category,Brands,Profile
from fastapi import HTTPException,Query
from utils.regular import password_hash,varify_password

from utils.regular import coustomer_authentication
import random
from fastapi.responses import StreamingResponse
import base64




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
    otp=db.query(Otp).filter(Otp.email==data.email).first()
    if otp:
        raise HTTPException(status_code=404,detail="already sent otp")
    
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not match your email")
    new_otp=random.randint(1111,9999)
    xyz=Otp(email=data.email,otp=new_otp)
    db.add(xyz)
    db.commit()
    return {"msg":f"sent otp this email {data.email},Otp {new_otp}"}


s=["@","#","$","&"]
def reset_password(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not match your email")
    coustomerotp=db.query(Otp).filter(Otp.email==data.email).first()
    if not coustomerotp:
        raise HTTPException(status_code=404,detail="not sent otp this email")
    if coustomerotp.otp==data.otp:
        for i in s:
            if i in data.new_password:
                if len(data.new_password)>=8:
                   new_hash=password_hash(data.new_password)
                   coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
                   coustomer.password=new_hash
                   db.commit()
                   db.refresh(coustomer)
                   db.delete(coustomerotp)
                   return {"msg":"reset your password"}
                raise HTTPException(status_code=404,detail="length of password is less than 8")
            raise HTTPException(status_code=404,detail="use special crackter in password")
    raise HTTPException(status_code=404,detail="not match your otp")
    
    
# def searching_product(page,limit,name,db:Session):
#     product=db.query(Product)
#     if product:
#         product=product.filter(Product.name.ilike(f"%{name}%"))
#     skip=int(page-1)*limit
#     data=product.offset(skip).limit(limit).all()
    
#     return {"page":page,
#             "limit":limit,
#             "data":data}    



def get_product(id,db:Session):
  product=db.query(Product).filter(Product.id==id).first()
  if not product:
      raise HTTPException(status_code=404,detail="not match your id ")
  
  return {"product":product.name,
          "mrp":product.mrp,
          "discount":product.discount_percentage,
          "sale_price":product.sale_price}


def category_get(db:Session):
    category=db.query(Category).all()
    if not category:
        raise HTTPException(status_code=404,detail="not found data")
    return category


def brand_get(db:Session):
    brand=db.query(Brands).all()
    if not brand:
        raise HTTPException(status_code=404,detail="not found data")
    return brand



def create_profile(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not match your id ")
    xyz=Profile(coustomer_id=data.coustomer_id,
                name=coustomer.name,
                email=coustomer.email,
                mob=data.mob,
                state=data.state,
                pin_code=data.pin_code,
                city=data.city,
                address=data.address)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":"create your profile"}


def get_profile(id,db:Session):
    profile=db.query(Profile).filter(Profile.coustomer_id==id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="not match your id ")
    return profile

