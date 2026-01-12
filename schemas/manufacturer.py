from pydantic import BaseModel
from typing import Optional



# Manufacturer Register

class ManufactureRegisterSchemas(BaseModel):
    store_name:str
    name:str
    email:str
    password:str


# Manufacturer Login

class MnaufacturerLoginSchemas(BaseModel):
    email:str
    password:str

# Product Create    

class ProductCreateSchemas(BaseModel):
    manufacturer_id:int
    name:str
    weight:str
    category:str
    brand:str
    quantity:int
    mrp:int
    discount_percentage:int


#Change Password

class ChangePasswordManufacturer(BaseModel):
    manufacturer_id:int
    old_password:str
    new_password:str


# Sent Opt

class ManufacturerOtpSchemas(BaseModel):
        email:str


# Reset Password

class ResetPasswordManufacturer(BaseModel):
     email:str
     otp:int
     new_password:str        


# MAnuafcturer Profile

class ProfileManufacturerSchemas(BaseModel):
    manufacturer_id:int
    mob:int
    state:str
    pin_code:int
    city:str
    address:str  


# Update manufacturer

class UpdateManufacturerProfleSchemas(BaseModel):
        name:Optional[str]=None
        email:Optional[str]=None
        mob:Optional[str]=None
        state:Optional[str]=None
        pin_code:Optional[str]=None
        city:Optional[str]=None
        address:Optional[str]=None 


        
#increase Product Quantity

class IncreaseQuantity (BaseModel):
     increase_quantity:str
                 

                 