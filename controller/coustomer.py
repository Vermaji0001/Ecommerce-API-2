
from sqlalchemy.orm import Session
from modals.all_modals import Coustomer,Otp,Product,Category,Brands,Profile,Wishlist,AddToCart,CreateOrder,KYCdetails,Notification,RateUs
from fastapi import HTTPException,Query,UploadFile
from utils.regular import password_hash,varify_password,create_token
from env.private_data import EXPIRY_MINUTES
from utils.regular import coustomer_authentication
import random
from datetime import timedelta
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import StreamingResponse
import io




#Coustomer Register

s=["@","#","$","&"]
def coustomer_register(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if coustomer:
        raise HTTPException (status_code=404,detail="Your email is already exists")
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
                return {"Msg","Register Successfully"}
              raise HTTPException (status_code=404,detail="Entre Your DOB")
           raise HTTPException(status_code=404,detail="Your password length is less than 8 ")
    raise HTTPException (status_code=404,detail="Use speacial crackter in password @,#,$,&")


#Coustomer Login

def coustomer_login(data,db:Session):
     verify=coustomer_authentication(data.email,data.password,db)
     if not verify:
         raise HTTPException(status_code=404,detail="invalid information")
     token=create_token(data={"sub":str(verify.id)},expire=timedelta(minutes=EXPIRY_MINUTES))
     return {"msg":" Successfully Login",
             "token_URL":token}


# Change Password

s=["@","#","$","&"]
def change_password(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect id")
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
     raise HTTPException(status_code=404,detail="Use special crackter in password @,#,$,&")
    raise HTTPException(status_code=404,detail="Not match your old password")
    


# Sent Opt on Email

def sent_opt(data,db:Session):
    otp=db.query(Otp).filter(Otp.email==data.email).first()
    if otp:
        raise HTTPException(status_code=404,detail="Already sent otp")
    
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect email")
    new_otp=random.randint(1111,9999)
    xyz=Otp(email=data.email,otp=new_otp)
    db.add(xyz)
    db.commit()
    return {"msg":f"sent otp this email {data.email},Otp {new_otp}"}


# Reset Password

s=["@","#","$","&"]
def reset_password(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.email==data.email).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect Email")
    coustomerotp=db.query(Otp).filter(Otp.email==data.email).first()
    if not coustomerotp:
        raise HTTPException(status_code=404,detail="Incorrect Email")
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
            raise HTTPException(status_code=404,detail="Use special crackter in password @,#,$,&")
    raise HTTPException(status_code=404,detail="InCorrect otp")
    
    
# def searching_product(page,limit,name,db:Session):
#     product=db.query(Product)
#     if product:
#         product=product.filter(Product.name.ilike(f"%{name}%"))
#     skip=int(page-1)*limit
#     data=product.offset(skip).limit(limit).all()
    
#     return {"page":page,
#             "limit":limit,
#             "data":data}    


 
#Get product
 
def get_product(id,db:Session):
  product=db.query(Product).filter(Product.id==id).first()
  if not product:
      raise HTTPException(status_code=404,detail="Incorrect id ")
  
  return {
          "product":product.name,
          "mrp":product.mrp,
          "discount":product.discount_percentage,
          "sale_price":product.sale_price}



# Get All Category

def category_get(db:Session):
    category=db.query(Category).all()
    if not category:
        raise HTTPException(status_code=404,detail="Not found Data")
    return category

 #Get all Brand

def brand_get(db:Session):
    brand=db.query(Brands).all()
    if not brand:
        raise HTTPException(status_code=404,detail="Not found data")
    return brand


# Craete Profile

def create_profile(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect Id ")
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
    return {"msg":"Create your profile"}


# Get profile

def get_profile(id,db:Session):
    profile=db.query(Profile).filter(Profile.coustomer_id==id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="not match your id ")
    return profile



# Add product in wishlist

def wishlist_product(data,db:Session):
     coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
     if not coustomer:
         raise HTTPException(status_code=404,detail="Incorrect Id")
     product=db.query(Product).filter(Product.id==data.product_id).first()
     if not product:
         raise HTTPException(status_code=404,detail="Incorrect id")
     wishlist=db.query(Wishlist)
     if wishlist.filter(Wishlist.coustomer_id==data.coustomer_id).first() and wishlist.filter(Wishlist.product_id==data.product_id).first():
         raise HTTPException(status_code=404,detail="Your product is already wishlist")
     xyz=Wishlist(coustomer_id=data.coustomer_id,product_id=data.product_id)
     db.add(xyz)
     db.commit()
     db.refresh(xyz)
     return {"msg":"Add product in wishlist"}


# Product add to cart

def add_to_cart(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    product=db.query(Product).filter(Product.id==data.product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="incorrect Id")
    addtocart=db.query(AddToCart)
    if addtocart.filter(AddToCart.coustomer_id==data.coustomer_id).first() and addtocart.filter(AddToCart.product_id==data.product_id).first():
        raise HTTPException(status_code=404,detail="Already add to cart this product")
    if product.quantity-data.product_quantity>=0:
        xyz=AddToCart(coustomer_id=data.coustomer_id,product_id=data.product_id,product_quantity=data.product_quantity)
        db.add(xyz)
        db.commit()
        db.refresh(xyz)
        return {"msg":"add your product"}
    raise HTTPException(status_code=404,detail="OUt Of Stock")



# Create order

orderstatus="your order is done"
payment_modes="cash on delivery"
def create_order(data,db:Session):
    try:  
      coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
      if not coustomer:
          raise HTTPException(status_code=404,detail="Inorrect Id")
      addtocarts=db.query(AddToCart).filter(AddToCart.coustomer_id==data.coustomer_id).first()
      if not addtocarts:
        raise HTTPException(status_code=404,detail=" Before add to cart")
      product=db.query(Product).filter(Product.id==addtocarts.product_id).first()
      if not product:
        raise HTTPException(status_code=404,detail="Not found data")
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
      return {"msg":"Your order is placed",
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
        raise HTTPException(status_code=404,detail="Something went wrong")
        






# cancel Order

def cancel_order(data,db:Session):
    order=db.query(CreateOrder).filter(CreateOrder.coustomer_id==data.coustomer_id).first()
    if not order:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    product=db.query(Product).filter(Product.id==order.product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    product.quantity=product.quantity+order.product_quantity
    db.commit()
    db.delete(order)
    db.commit()
    return {"Msg":"Cancel your order"}
    


# Get All Order   

def get_all_order(id,db:Session):
    order=db.query(CreateOrder).filter(CreateOrder.coustomer_id==id).all()
    if not order:
        raise HTTPException(status_code=404,detail="Inorrect Id")
    return order


# Delete Coustomer

def delete_coustomer(id,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    db.delete(coustomer)
    db.commit()
    return {"Msg":"Delete coustomer"}



# Upload kyc details

notification="Complete your kyc"
async def kyc_detail(coustomer_id,document_image:UploadFile,account_holder_name,account_number,confirm_acc_number,ifsc_code,db:Session):
    coustomer=db.query(KYCdetails).filter(KYCdetails.coustomer_id==coustomer_id).first()
    if coustomer:
        raise HTTPException(status_code=404,detail="already compelete your KYC")
    profile=db.query(Profile).filter(Profile.coustomer_id==coustomer_id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="Please create profile")
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
    raise HTTPException(status_code=404,detail="Incorrect Your confirm account number")


# Get All Notification

def get_all_notification(id,db:Session):
    notification=db.query(Notification).filter(Notification.coustomer_id==id).all()
    if not notification:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    return notification


# Review On Product

def review_on_product(data,db:Session):
    coustomer=db.query(Coustomer).filter(Coustomer.id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    coustomer=db.query(CreateOrder).filter(CreateOrder.coustomer_id==data.coustomer_id).first()
    if not coustomer:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    xyz=RateUs(coustomer_id=data.coustomer_id,product_id=coustomer.product_id,rate_us=data.rate_us)
    db.add(xyz)
    db.commit()
    db.refresh(xyz)
    return {"msg":"Submit your review"}


# Cancel addtocart    
def cencel_add_to_cart(id,db:Session):
    addtocart=db.query(AddToCart).filter(AddToCart.coustomer_id==id).first()
    if not addtocart:
        raise HTTPException(status_code=404,detail="Incorrect Id")
    db.delete(addtocart)
    db.commit()
    return {"Msg":"Delete your cart"}



# Profile Update

def profile_update(id,data,db:Session):
    profile=db.query(Profile).filter(Profile.coustomer_id==id).first()
    if not profile:
        raise HTTPException(status_code=404,detail="Please create profile")
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
        raise HTTPException(status_code=404,detail="Incorrect Id")
    coustomer.name=data.name
    coustomer.email=data.email
    db.commit()
    return {"Msg":"Change your data"}