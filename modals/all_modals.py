
from sqlalchemy import Column,String,Integer,Date
from utils.maindata import Base
from sqlalchemy import LargeBinary




class Coustomer(Base):
    __tablename__="registercoustomer"
    id=Column(Integer,primary_key=True)
    name=Column(String(200),nullable=False)
    email=Column(String(20),nullable=False)
    password=Column(String(200),nullable=False)
    dob=Column(String(20),nullable=False)
    referal_code=Column(String(10),nullable=True)



class Manufacturer(Base):
    __tablename__="manufacturerregister"
    id=Column(Integer,primary_key=True)
    store_name=Column(String(200),nullable=False)
    name=Column(String(200),nullable=False)
    email=Column(String(200),nullable=False)
    password=Column(String(200),nullable=False)


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