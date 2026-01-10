from pydantic import BaseModel ,EmailStr
from typing import Optional



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


class KYCschemas(BaseModel):
    coustomer_id:int
    account_holder_name:str
    account_number:int
    account_acc_number:int
    ifsce_code:str  


class RateUsSchemas(BaseModel):
    coustomer_id:int
    rate_us:str      


class UpdateProfleSchemas(BaseModel):
        name:Optional[str]=None
        email:Optional[str]=None
        mob:Optional[str]=None
        state:Optional[str]=None
        pin_code:Optional[str]=None
        city:Optional[str]=None
        address:Optional[str]=None