from fastapi import APIRouter,Depends
from schemas.coustomer import CoustomerRegisterSchemas,CoustomerLogin,ChangePasswordSchemas,OtpSentSchemas,ResetPasswordSchemas
from sqlalchemy.orm import Session
from utils.maindata import get_db
from controller.coustomer import coustomer_register,coustomer_login,change_password,sent_opt,reset_password


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