from fastapi import APIRouter,Depends,Query
from schemas.coustomer import CoustomerRegisterSchemas,CoustomerLogin,ChangePasswordSchemas,OtpSentSchemas,ResetPasswordSchemas,ProfileSchemas
from sqlalchemy.orm import Session
from utils.maindata import get_db
from controller.coustomer import coustomer_register,coustomer_login,change_password,sent_opt,reset_password,get_product,category_get,brand_get,create_profile,get_profile


router=APIRouter()


@router.post("/coustomerregister")
def register_coustomer(data:CoustomerRegisterSchemas,db:Session=Depends(get_db)):
    final=coustomer_register(data,db)
    return final

@router.get("/coustomerlogin")
def login_coustomer(data:CoustomerLogin,db:Session=Depends(get_db)):
    final=coustomer_login(data,db)
    return final



@router.patch("/changepassword")
def passowrd_change(data:ChangePasswordSchemas,db:Session=Depends(get_db)):
    final=change_password(data,db)
    return final


@router.post("/sentotp")
def otp_sent(data:OtpSentSchemas,db:Session=Depends(get_db)):
    final=sent_opt(data,db)
    return 

@router.patch("/resetpassword")
def password_reset(data:ResetPasswordSchemas,db:Session=Depends(get_db)):
    final=reset_password(data,db)
    return final

@router.get("/getproduct/{id}")
def product_searching(id:int,db:Session=Depends(get_db)):
    final=get_product(id,db)
    return final

@router.get("/getcategory")
def get_category(db:Session=Depends(get_db)):
    final=category_get(db)
    return final



@router.get("/getbrand")
def get_brand(db:Session=Depends(get_db)):
    final=brand_get(db)
    return final


@router.post("/profile")
def profile_create(data:ProfileSchemas,db:Session=Depends(get_db)):
    final=create_profile(data,db)
    return final

@router.get("/getprofile/{id}")
def profile_get_by_id(id:int,db:Session=Depends(get_db)):
    final=get_profile(id,db)
    return final