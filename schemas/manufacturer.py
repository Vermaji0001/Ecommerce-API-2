from pydantic import BaseModel
from sqlalchemy import LargeBinary

class ManufactureRegisterSchemas(BaseModel):
    store_name:str
    name:str
    email:str
    password:str


class MnaufacturerLoginSchemas(BaseModel):
    email:str
    password:str

class ProductCreateSchemas(BaseModel):
    manufacturer_id:int
    name:str
    weight:str
    category:str
    brand:str
    quantity:int
    mrp:int
    discount_percentage:int
