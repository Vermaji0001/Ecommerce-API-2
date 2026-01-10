from sqlalchemy.orm import Session
from modals.all_modals import Manufacturer,Category,Brands,OtpManufacturer,ProfileManufacturer
from fastapi import HTTPException
from modals.all_modals import Product
from fastapi import UploadFile,File,Form,Query
from sqlalchemy.exc import SQLAlchemyError
from utils.regular import password_hash,manufacturer_authentication,varify_password
import random
from schemas.coustomer import UpdateProfleSchemas
from datetime import datetime


s=["@","#","$","&"]
def manufacturer_register(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.store_name==data.store_name).first()
    if manufacturer:
        raise HTTPException (status_code=404,detail="your is store name  is already exists")
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if manufacturer:
        raise HTTPException(status_code=404,detail="your email is already exists")
    for i in s:
        if i in data.password:
            if len(data.password)>=8:
                hash_pass=password_hash(data.password)
                time=datetime.now()
                xyz=Manufacturer(store_name=data.store_name,name=data.name,email=data.email,password=hash_pass,created_at=time)
                db.add(xyz)
                db.commit()
                db.refresh(xyz)
                return {"msg":"manufacturer is register"}
            raise HTTPException (status_code=404,detail="your password lenght is less than 8 ")
    raise HTTPException   (status_code=404,detail="use special crackter in password") 

def manufacturer_login(data,db:Session):
    manufacturer=manufacturer_authentication(data.email,data.password,db)
    if not manufacturer:
        raise HTTPException (status_code=404,detail="invalid information")
    return {"msg":"manufacturer login"}




async def product_create(manufacturer_id,name,weight,category,brand,quantity,mrp,discount_percentage,file:UploadFile,db:Session):
  try:
    manfacturer=db.query(Manufacturer).filter(Manufacturer.id==manufacturer_id).first()
    if not manfacturer:
        raise HTTPException(status_code=404,detail="manufacturer not register")  
    if not file:
        raise HTTPException(status_code=404,detail="not image")
    product=db.query(Product).filter(Product.name==name).first()
    if product:
        raise HTTPException(status_code=404,detail="your product is already exists")
    new_image=await file.read()
    discount_price=mrp*discount_percentage/100
    sale_price=mrp-discount_price
    xyz=Product(manufacturer_id=manufacturer_id,
        image=new_image,
                name=name,
                weight=weight,
                category=category,
                brand=brand,
                quantity=quantity,
                mrp=mrp,
                discount_percentage=discount_percentage,
                sale_price=sale_price)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    categorys=db.query(Category).filter(Category.name==name).first()
    if not categorys:
        xyz=Category(name=category)
        db.add(xyz)
        db.commit()
        
    brands=db.query(Brands).filter(Brands.name==brand).first()
    if not brands:
        xyz=Brands(name=brand)
        db.add(xyz)
        db.commit()
        return {"msg":"create product"}
    return {"msg":"create product"}
  except SQLAlchemyError:
      db.rollback()
      raise HTTPException (status_code=404,detail="error")

    

s=["@","#","$","&"]
def change_password_manufacturer(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==data.manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="not match your id ")
    if varify_password(data.old_password,manufacturer.password):
     for i in s:
        if i in data.new_password:
            if len(data.new_password)>=8:
                new_hash=password_hash(data.new_password)
                manufacturer.password=new_hash
                db.commit()
                db.refresh(manufacturer)
                return{"msg":"change your password"}
            raise HTTPException(status_code=404,detail="your length of passwod is less than 8")
     raise HTTPException(status_code=404,detail="use special crackter in password")
    raise HTTPException(status_code=404,detail="not match your old password")
    
    
    
    

def sent_opt_manufacturer(data,db:Session):
    otp=db.query(OtpManufacturer).filter(OtpManufacturer.email==data.email).first()
    if otp:
        raise HTTPException(status_code=404,detail="already sent otp")
    
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="not match your email")
    new_otp=random.randint(1111,9999)
    xyz=OtpManufacturer(email=data.email,otp=new_otp)
    db.add(xyz)
    db.commit()
    return {"msg":f"sent otp this email {data.email},Otp {new_otp}"}




s=["@","#","$","&"]
def reset_password_manufacturer(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="not match your email")
    manufacturerotp=db.query(OtpManufacturer).filter(OtpManufacturer.email==data.email).first()
    if not manufacturerotp:
        raise HTTPException(status_code=404,detail="not sent otp this email")
    if manufacturerotp.otp==data.otp:
        for i in s:
            if i in data.new_password:
                if len(data.new_password)>=8:
                   new_hash=password_hash(data.new_password)
                   manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
                   manufacturer.password=new_hash
                   db.commit()
                   db.refresh(manufacturer)
                   db.delete(manufacturerotp)
                   return {"msg":"reset your password"}
                raise HTTPException(status_code=404,detail="length of password is less than 8")
            raise HTTPException(status_code=404,detail="use special crackter in password")
    raise HTTPException(status_code=404,detail="not match your otp")





def create_profile_manufacturer(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==data.manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="not match your id ")
    xyz=ProfileManufacturer(manufacturer_id=data.manufacturer_id,
                name=manufacturer.name,
                email=manufacturer.email,
                mob=data.mob,
                state=data.state,
                pin_code=data.pin_code,
                city=data.city,
                address=data.address)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":"create your  manufacturer profile"}


def get_profile_manufacturer(id,db:Session):
    manufacturer=db.query(ProfileManufacturer).filter(ProfileManufacturer.manufacturer_id==id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="not match your id ")
    return manufacturer


def delete_manufacturer(id,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="not manufacturer")
    db.delete(manufacturer)
    db.commit()
    return {"msg":"delete manufacturer"}



def delete_product(id,db:Session):
    product=db.query(Product).filter(Product.id==id).first()
    if not product:
        raise HTTPException(status_code=404,detail="not match your product id ")
    db.delete(product)
    db.commit()
    return {"msg":"delete your product"}



def profile_update_manufacturer(id,data,db:Session):
    profile=db.query(ProfileManufacturer).filter(ProfileManufacturer.manufacturer_id==id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="please create profile")
    profile.name=data.name
    profile.email=data.email
    profile.mob=data.mob
    profile.state=data.state
    profile.pin_code=data.pin_code
    profile.city=data.city
    profile.address=data.address
    db.commit()
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="not match your coustomer")
    manufacturer.name=data.name
    manufacturer.email=data.email
    db.commit()
    return {"msg":"change manufacturer data"} 




   