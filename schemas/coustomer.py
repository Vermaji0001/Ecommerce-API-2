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

