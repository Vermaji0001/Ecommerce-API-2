from pydantic import BaseModel ,EmailStr



class CoustomerRegisterSchemas(BaseModel):
    name:str
    email:EmailStr
    password:str
    dob:str
    referal_code:str

class CoustomerLogin(BaseModel):
    email:str
    password:str

class ChangePasswordSchemas(BaseModel):
    coustomer_id:int
    old_password:str
    new_password:str  

class OtpSentSchemas(BaseModel):
    email:str


class ResetPasswordSchemas(BaseModel):
    email:str
    otp:int
    new_password:str    

class ProfileSchemas(BaseModel):
    coustomer_id:int
    
    mob:int
    state:str
    pin_code:int
    city:str
    address:str


class WishlistSchemas(BaseModel):
    coustomer_id:int
    product_id:int  


class AddtoCartSchemas(BaseModel):
    coustomer_id:int
    product_id:int
    product_quantity:int


class OderSchemas(BaseModel):
    coustomer_id:int

class OrderCencelSchemas(BaseModel):
    coustomer_id:int    