
from sqlalchemy.orm import Session
from modals.all_modals import Coustomer,Otp,Product,Category,Brands,Profile,Wishlist,AddToCart,CreateOrder,KYCdetails,Notification,RateUs
from fastapi import HTTPException,Query,UploadFile
from utils.regular import password_hash,varify_password

from utils.regular import coustomer_authentication
import random

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import StreamingResponse
import io




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
                time=datetime.now()
                xyz=Coustomer(name=data.name,
                          email=data.email,
                          password=hash_password,
                          dob=data.dob,
                          referal_code=data.referal_code,
                          created_at=time)
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
  image=StreamingResponse(io.BytesIO(product.image))
  return {
          "product_image":image,
          "product":product.name,
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





notification="complete your kyc"
async def kyc_detail(coustomer_id,document_image:UploadFile,account_holder_name,account_number,confirm_acc_number,ifsc_code,db:Session):
    coustomer=db.query(KYCdetails).filter(KYCdetails.coustomer_id==coustomer_id).first()
    if coustomer:
        raise HTTPException(status_code=404,detail="already compelete your KYC")
    profile=db.query(Profile).filter(Profile.coustomer_id==coustomer_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="please create profile")
    image=await document_image.read()
    if account_number==confirm_acc_number:
        xyz=KYCdetails(coustomer_id=coustomer_id,
                   name=profile.name,
                   mob=profile.mob,
                   email=profile.email,
                   pin_code=profile.pin_code,
                   document_image=image,
                   account_holder_name=account_holder_name,account_number=account_number,ifsc_code=ifsc_code)
        db.add(xyz)
        db.commit()
        db.refresh(xyz)
        xyz=Notification(coustomer_id=coustomer_id,notification=notification)
        db.add(xyz)
        db.commit()
        db.refresh(xyz)
        return {"msg":"complete your KYC"}
    raise HTTPException(status_code=404,detail="not match your acoount number ")
    
def get_all_notification(id,db:Session):
    notification=db.query(Notification).filter(Notification.coustomer_id==id).all()
    if not notification:
        raise HTTPException(status_code=404,detail="not match your id ")
    return notification


def review_on_product(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not register coustomer")
    coustomer=db.query(CreateOrder).filter(CreateOrder.coustomer_id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not order")
    xyz=RateUs(coustomer_id=data.coustomer_id,product_id=coustomer.product_id,rate_us=data.rate_us)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":"submit your review"}
    
def cencel_add_to_cart(id,db:Session):
    addtocart=db.query(AddToCart).filter(AddToCart.coustomer_id==id).first()
    if not addtocart:
        raise HTTPException(status_code=404,detail="not add to cart")
    db.delete(addtocart)
    db.commit()
    return {"msg":"delete your cart"}





def profile_update(id,data,db:Session):
    profile=db.query(Profile).filter(Profile.coustomer_id==id).first()
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
    coustomer=db.query(Coustomer).filter(Coustomer.id==id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="not match your coustomer")
    coustomer.name=data.name
    coustomer.email=data.email
    db.commit()
    return {"msg":"change your data"}