from pydantic import BaseModel ,EmailStr
from typing import Optional


#Coustomer Register

class CoustomerRegisterSchemas(BaseModel):
    name:str
    email:EmailStr
    password:str
    dob:str
    referal_code:str

#Coustomer Login

class CoustomerLogin(BaseModel):
    email:str
    password:str


# Change Password    

class ChangePasswordSchemas(BaseModel):
    coustomer_id:int
    old_password:str
    new_password:str  



# Sent Opt on Email    

class OtpSentSchemas(BaseModel):
    email:str


# Reset Password

class ResetPasswordSchemas(BaseModel):
    email:str
    otp:int
    new_password:str   



# Craete Profile

class ProfileSchemas(BaseModel):
    coustomer_id:int
    mob:int
    state:str
    pin_code:int
    city:str
    address:str


# Add product in wishlist

class WishlistSchemas(BaseModel):
    coustomer_id:int
    product_id:int  



# Product add to cart

class AddtoCartSchemas(BaseModel):
    coustomer_id:int
    product_id:int
    product_quantity:int





# Create order

class OderSchemas(BaseModel):
    coustomer_id:int







# Cancel order

class OrderCencelSchemas(BaseModel):
    coustomer_id:int    





# KYC details

class KYCschemas(BaseModel):
    coustomer_id:int
    account_holder_name:str
    account_number:int
    account_acc_number:int
    ifsce_code:str  



#Rate Us

class RateUsSchemas(BaseModel):
    coustomer_id:int
    rate_us:str      



# Update Profile

class UpdateProfleSchemas(BaseModel):
        name:Optional[str]=None
        email:Optional[str]=None
        mob:Optional[str]=None
        state:Optional[str]=None
        pin_code:Optional[str]=None
        city:Optional[str]=None
        address:Optional[str]=None