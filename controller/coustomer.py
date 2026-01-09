
from sqlalchemy.orm import Session
from modals.all_modals import Coustomer,Otp,Product,Category,Brands,Profile,Wishlist,AddToCart,CreateOrder
from fastapi import HTTPException,Query
from utils.regular import password_hash,varify_password

from utils.regular import coustomer_authentication
import random

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError




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

def wishlist_product(data,db:Session):
     coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
     if not coustomer:
         raise HTTPException(status_code=404,detail="not match your id")
     product=db.query(Product).filter(Product.id==data.product_id).first()
     if not product:
         raise HTTPException(status_code=404,detail="not product")
     wishlist=db.query(Wishlist)
     if wishlist.filter(Wishlist.coustomer_id==data.coustomer_id).first() and wishlist.filter(Wishlist.product_id==data.product_id).first():
         raise HTTPException(status_code=404,detail="your product is already wishlist")
     xyz=Wishlist(coustomer_id=data.coustomer_id,product_id=data.product_id)
     db.add(xyz)
     db.commit()
     db.refresh(xyz)
     return {"msg":"add wishlist your product"}



def add_to_cart(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not  match your coustomer id ")
    product=db.query(Product).filter(Product.id==data.product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="not match your product id ")
    addtocart=db.query(AddToCart)
    if addtocart.filter(AddToCart.coustomer_id==data.coustomer_id).first() and addtocart.filter(AddToCart.product_id==data.product_id).first():
        raise HTTPException(status_code=404,detail="already add to cart this product")
    if product.quantity-data.product_quantity>=0:
        xyz=AddToCart(coustomer_id=data.coustomer_id,product_id=data.product_id,product_quantity=data.product_quantity)
        db.add(xyz)
        db.commit()
        db.refresh(xyz)
        return {"msg":"add your product"}
    raise HTTPException(status_code=404,detail="out of stock this product")




orderstatus="your order is done"
payment_modes="cash on delivery"
def create_order(data,db:Session):
    try:  
      coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
      if not coustomer:
          raise HTTPException(status_code=404,detail="not match your cosutomer id ")
      addtocarts=db.query(AddToCart).filter(AddToCart.coustomer_id==data.coustomer_id).first()
      if not addtocarts:
        raise HTTPException(status_code=404,detail="please add to cart ")
      product=db.query(Product).filter(Product.id==addtocarts.product_id).first()
      if not product:
        raise HTTPException(status_code=404,detail="not found data")
      time=datetime.now()
      discount_on_products=(product.mrp*product.discount_percentage/100)*addtocarts.product_quantity
      total_prices=(product.mrp-discount_on_products)*addtocarts.product_quantity
      xyz=CreateOrder(coustomer_id=data.coustomer_id,
                      product_id=addtocarts.product_id,
                      product_name=product.name,
                      product_quantity=addtocarts.product_quantity,
                      payment_mode=payment_modes,
                      order_status=orderstatus,
                      mrp=product.mrp,
                      discount_on_product=discount_on_products,
                      total_price=total_prices,
                      ordered_at=time)
      db.add(xyz)
      db.flush()
      quantity=product.quantity-addtocarts.product_quantity
      product.quantity=quantity
      db.commit()
      db.delete(addtocarts)
      db.commit()
      return {"msg":"your order is placed",
              "coustomer_name":coustomer.name,
              "product_name":product.name,
              "product_quantity":addtocarts.product_quantity,
              "mrp":product.mrp,
              "total_price":total_prices,
              "discount_percentage":product.discount_percentage,
              "discount_on_product":discount_on_products,
              "msg":"THANK YOU for order"}
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=404,detail="something went wrong")

# s=100    
# def xyz(id,db:Session):
#     product=db.query(Product).filter(Product.id==id).first()
#     if product:
#         product.quantity=s
#         db.commit()
#         return {"xyz"}
#     raise HTTPException(status_code=404,detail="xyzzzzzzzzzzz")



def cancel_order(data,db:Session):
    order=db.query(CreateOrder).filter(CreateOrder.coustomer_id==data.coustomer_id).first()
    if not order:
        raise HTTPException(status_code=404,detail="not order")
    product=db.query(Product).filter(Product.id==order.product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="not match your id ")
    product.quantity=product.quantity+order.product_quantity
    db.commit()
    db.delete(order)
    db.commit()
    return {"cencel your order"}
    
    
def get_all_order(id,db:Session):
    order=db.query(CreateOrder).filter(CreateOrder.coustomer_id==id).all()
    if not order:
        raise HTTPException(status_code=404,detail="not match id ")
    return order


def delete_coustomer(id,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not coustomer")
    db.delete(coustomer)
    db.commit()
    return {"delete coustomer"}
