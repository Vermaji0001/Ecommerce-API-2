
from sqlalchemy import Column,String,Integer,Date
from utils.maindata import Base
from sqlalchemy import LargeBinary,TIMESTAMP





class Coustomer(Base):
    __tablename__="registercoustomer"
    id=Column(Integer,primary_key=True)
    name=Column(String(200),nullable=False)
    email=Column(String(20),nullable=False)
    password=Column(String(200),nullable=False)
    dob=Column(String(20),nullable=False)
    referal_code=Column(String(10),nullable=True)
    created_at=Column(TIMESTAMP,nullable=False)



class Manufacturer(Base):
    __tablename__="manufacturerregister"
    id=Column(Integer,primary_key=True)
    store_name=Column(String(200),nullable=False)
    name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False)
    password=Column(String(200),nullable=False)
    created_at=Column(TIMESTAMP,nullable=False)


class Product(Base):
    __tablename__="product"
    id=Column(Integer,primary_key=True)
    manufacturer_id=Column(Integer,nullable=False)
    image=Column(LargeBinary,nullable=False)
    name=Column(String(200),nullable=False)
    weight=Column(String(200),nullable=False)
    category=Column(String(200),nullable=False)
    brand=Column(String(200),nullable=False)
    quantity=Column(Integer,nullable=False)
    mrp=Column(Integer,nullable=False)
    discount_percentage=Column(Integer,nullable=False)
    sale_price=Column(Integer,nullable=True)

class Category(Base):
    __tablename__="category"
    id=Column(Integer,primary_key=True)
    name=Column(String(200),nullable=False)


class Brands(Base):
    __tablename__="brands"
    id=Column(Integer,primary_key=True)
    name=Column(String(200),nullable=False)


class Otp(Base):
    __tablename__="otp"
    id=Column(Integer,primary_key=True)
    email=Column(String(200),nullable=False)
    otp=Column(Integer,nullable=False)


class OtpManufacturer(Base):
    __tablename__="otpmanufacturer"
    id=Column(Integer,primary_key=True)
    email=Column(String(200),nullable=False)
    otp=Column(Integer,nullable=False)



class Profile(Base):
    __tablename__="profile"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False)
    mob=Column(String(20),nullable=False)
    state=Column(String(200),nullable=False)
    pin_code=Column(String(20),nullable=False)
    city=Column(String(200),nullable=False)
    address=Column(String(200),nullable=False)


class ProfileManufacturer(Base):
    __tablename__="profilemanufacturer"
    id=Column(Integer,primary_key=True)
    manufacturer_id=Column(Integer,nullable=False)
    name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False)
    mob=Column(String(20),nullable=False)
    state=Column(String(200),nullable=False)
    pin_code=Column(String(20),nullable=False)
    city=Column(String(200),nullable=False)
    address=Column(String(200),nullable=False)


class Wishlist(Base):
    __tablename__="wishlist"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    product_id=Column(Integer,nullable=False)


class AddToCart(Base):
    __tablename__="addtocart"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    product_id=Column(Integer,nullable=False)
    product_quantity=Column(Integer,nullable=False)    



class CreateOrder(Base):
    __tablename__="order"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    product_id=Column(Integer,nullable=True)
    product_name=Column(String(200),nullable=True)
    product_quantity=Column(Integer,nullable=True)
    payment_mode=Column(String(200),nullable=False)
    order_status=Column(String(20),nullable=True)
    mrp=Column(Integer,nullable=True)
    discount_on_product=Column(Integer,nullable=True)
    total_price=Column(Integer,nullable=True)
    ordered_at=Column(TIMESTAMP,nullable=True)



class KYCdetails(Base):
    __tablename__="kycdetail"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    name=Column(String(200),nullable=False)
    mob=Column(String(20),nullable=False)
    email=Column(String(200),nullable=False)
    pin_code=Column(String(200),nullable=False)
    document_image=Column(LargeBinary,nullable=False)
    account_holder_name=Column(String(200),nullable=False)
    account_number=Column(Integer,nullable=False)
    ifsc_code=Column(String(200),nullable=False)


class Notification(Base):
    __tablename__='notification'
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    notification=Column(String(200),nullable=False)



class RateUs(Base):
    __tablename__="rateus"
    id=Column(Integer,primary_key=True)
    coustomer_id=Column(Integer,nullable=False)
    product_id=Column(Integer,nullable=False)
    rate_us=Column(String(5),nullable=False)    