from pydantic import BaseModel


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


class ChangePasswordManufacturer(BaseModel):
    manufacturer_id:int
    old_password:str
    new_password:str


class ManufacturerOtpSchemas(BaseModel):
        email:str

class ResetPasswordManufacturer(BaseModel):
     email:str
     otp:int
     new_password:str        


class ProfileManufacturerSchemas(BaseModel):
    manufacturer_id:int
    mob:int
    state:str
    pin_code:int
    city:str
    address:str     