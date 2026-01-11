from sqlalchemy.orm import Session
from modals.all_modals import Manufacturer,Category,Brands,OtpManufacturer,ProfileManufacturer
from fastapi import HTTPException
from modals.all_modals import Product
from fastapi import UploadFile,File,Form,Query
from sqlalchemy.exc import SQLAlchemyError
from utils.regular import password_hash,manufacturer_authentication,varify_password,create_token
from env.private_data import EXPIRY_MINUTES
import random

from datetime import timedelta,datetime






###################################################################################################################################

#Manufacturer Register

s=["@","#","$","&"]
def manufacturer_register(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.store_name==data.store_name).first()
    if manufacturer:
        raise HTTPException (status_code=404,detail="Store name is already exists")
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if manufacturer:
        raise HTTPException(status_code=404,detail="Your email is already exists")
    for i in s:
        if i in data.password:
            if len(data.password)>=8:
                hash_pass=password_hash(data.password)
                time=datetime.now()
                xyz=Manufacturer(store_name=data.store_name,name=data.name,email=data.email,password=hash_pass,created_at=time)
                db.add(xyz)
                db.commit()
                db.refresh(xyz)
                return {"msg":"Manufacturer Register Successfully"}
            raise HTTPException (status_code=404,detail="Your password lenght is less than 8 ")
    raise HTTPException   (status_code=404,detail="Use special crackter in password @,#,$,&")  




#Manufacturer Login

def manufacturer_login(data,db:Session):
    manufacturer=manufacturer_authentication(data.email,data.password,db)
    if not manufacturer:
        raise HTTPException (status_code=404,detail="invalid information")
    token=create_token(data={"sub":str(manufacturer.id)} ,expire=timedelta(minutes=EXPIRY_MINUTES))
    return {"msg":"Login Succesfully",
            "token":token}




#Create Product By Manufacturer

async def product_create(manufacturer_id,name,weight,category,brand,quantity,mrp,discount_percentage,file:UploadFile,db:Session):
  try:
    manfacturer=db.query(Manufacturer).filter(Manufacturer.id==manufacturer_id).first()
    if not manfacturer:
        raise HTTPException(status_code=404,detail="Manufacturer not exists")  
    if not file:
        raise HTTPException(status_code=404,detail="Image not found")
    product=db.query(Product).filter(Product.name==name).first()
    if product:
        raise HTTPException(status_code=404,detail="This Product is already Create")
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
        return {"msg":"Product create"}
    return {"msg":"Product create"}
  except SQLAlchemyError:
      db.rollback()
      raise HTTPException (status_code=404,detail="Something Went Wrong")
  


# Change Password by Manufacturer

s=["@","#","$","&"]
def change_password_manufacturer(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==data.manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Your id not exists")
    if varify_password(data.old_password,manufacturer.password):
     for i in s:
        if i in data.new_password:
            if len(data.new_password)>=8:
                new_hash=password_hash(data.new_password)
                manufacturer.password=new_hash
                db.commit()
                db.refresh(manufacturer)
                return{"msg":"change your password"}
            raise HTTPException(status_code=404,detail="Your length of passwod is less than 8")
     raise HTTPException(status_code=404,detail="Use special crackter in password @,#,$,&")
    raise HTTPException(status_code=404,detail="Old password wrong")



# Sent Otp on Manufacturer Email

def sent_opt_manufacturer(data,db:Session):
    otp=db.query(OtpManufacturer).filter(OtpManufacturer.email==data.email).first()
    if otp:
        raise HTTPException(status_code=404,detail="Otp already sent")
    
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Not match your email")
    new_otp=random.randint(1111,9999)
    xyz=OtpManufacturer(email=data.email,otp=new_otp)
    db.add(xyz)
    db.commit()
    return {"msg":f"sent otp this email {data.email},Otp {new_otp}"}


# Reset password By manufacturer

s=["@","#","$","&"]
def reset_password_manufacturer(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.email==data.email).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Incorrect Email")
    manufacturerotp=db.query(OtpManufacturer).filter(OtpManufacturer.email==data.email).first()
    if not manufacturerotp:
        raise HTTPException(status_code=404,detail="Incorrect Email")
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
                   return {"msg":"Reset your password"}
                raise HTTPException(status_code=404,detail="length of password is less than 8")
            raise HTTPException(status_code=404,detail="Use special crackter in password @,#,$,&")
    raise HTTPException(status_code=404,detail="Incorrect Otp")



# Create Manufacturer Profile

def create_profile_manufacturer(data,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==data.manufacturer_id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Incorrect Manufacturer Id")
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
    return {"msg":"Create  Manufacturer Profile"}



# Get Mnaufacturer profile

def get_profile_manufacturer(id,db:Session):
    manufacturer=db.query(ProfileManufacturer).filter(ProfileManufacturer.manufacturer_id==id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    return manufacturer


# delete manufacturer

def delete_manufacturer(id,db:Session):
    manufacturer=db.query(Manufacturer).filter(Manufacturer.id==id).first()
    if not manufacturer:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    db.delete(manufacturer)
    db.commit()
    return {"msg":"Delete manufacturer"}



# Delete Product

def delete_product(id,db:Session):
    product=db.query(Product).filter(Product.id==id).first()
    if not product:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    db.delete(product)
    db.commit()
    return {"msg":"Delete your product"}



# Manufacturer Profile Update

def profile_update_manufacturer(id,data,db:Session):
    profile=db.query(ProfileManufacturer).filter(ProfileManufacturer.manufacturer_id==id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="Incorrect Id")
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
        raise HTTPException(status_code=404,detail="Incorrect Id")
    manufacturer.name=data.name
    manufacturer.email=data.email
    db.commit()
    return {"msg":"Update Manufacturer Profile"} 




def increase_quantity(id,data,db:Session):
    product=db.query(Product).filter(Product.id==id).first()
    if product:
        product.quantity=data.increase_quantity
        db.commit()
        return {"Msg":"update Product Quantity"}
    raise HTTPException(status_code=404,detail="NOt found Data")
