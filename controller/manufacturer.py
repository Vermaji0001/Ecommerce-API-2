from sqlalchemy.orm import Session
from modals.all_modals import Manufacturer,Category,Brands
from fastapi import HTTPException
from modals.all_modals import Product
from fastapi import UploadFile,File,Form,Query
from sqlalchemy.exc import SQLAlchemyError
from utils.regular import password_hash,manufacturer_authentication



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
                xyz=Manufacturer(store_name=data.store_name,name=data.name,email=data.email,password=hash_pass)
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

    
    
    
    



