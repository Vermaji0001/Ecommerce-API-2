from fastapi import APIRouter,Depends,UploadFile,File,Form
from schemas.manufacturer import ManufactureRegisterSchemas,MnaufacturerLoginSchemas,ChangePasswordManufacturer,ManufacturerOtpSchemas,ResetPasswordManufacturer,ProfileManufacturerSchemas,UpdateManufacturerProfleSchemas
from controller.manufacturer import manufacturer_register,manufacturer_login,product_create,change_password_manufacturer,sent_opt_manufacturer,reset_password_manufacturer,create_profile_manufacturer,get_profile_manufacturer,delete_manufacturer,delete_product,profile_update_manufacturer
from sqlalchemy.orm  import Session
from utils.maindata import get_db


router=APIRouter()


@router.post("/manufacturerregister")
def register_manufacturer(data:ManufactureRegisterSchemas,db:Session=Depends(get_db)):
    final=manufacturer_register(data,db)
    return final


@router.get("/manufacturerlogin")
def login_manufacturer(data:MnaufacturerLoginSchemas,db:Session=Depends(get_db)):
    final=manufacturer_login(data,db)
    return final

@router.post("/createproduct")
async def craete_product(manufacturer_id:int=Form(...),
                   name:str=Form(...),
                   weight:str=Form(...),
                   category:str=Form(...),
                   brand:str=Form(...),
                   quantity:int=Form(...),
                   mrp:int=Form(...),
                   discount_percentage:int=Form(...),
                   file:UploadFile=File(...),
                   db:Session=Depends(get_db)):
    final= await product_create(manufacturer_id,name,weight,category,brand,quantity,mrp,discount_percentage,file,db)
    return final


@router.patch("/changepasswordmanufacturer")
def manufacturer_change_password(data:ChangePasswordManufacturer,db:Session=Depends(get_db)):
    final=change_password_manufacturer(data,db)
    return final

@router.post("/otpsentmanufacturer")
def manufacturer_otp_sent(data:ManufacturerOtpSchemas,db:Session=Depends(get_db)):
    final=sent_opt_manufacturer(data,db)
    return final


@router.patch("/resetpassowrdmanufacturer")
def manufacturer_reset_password(data:ResetPasswordManufacturer,db:Session=Depends(get_db)):
    final=reset_password_manufacturer(data,db)
    return final


@router.post("/manufacturerprofile")
def manufacturer_profile(data:ProfileManufacturerSchemas,db:Session=Depends(get_db)):
    final=create_profile_manufacturer(data,db)
    return final    


@router.get("/getmanufacturerprofile/{id}")
def get_manufacturer_profile(id:int,db:Session=Depends(get_db)):
     final=get_profile_manufacturer(id,db)
     return final

@router.delete("/deletemanufacturer/{id}")
def manufacturer_delete(id:int,db:Session=Depends(get_db)):
    final=delete_manufacturer(id,db)
    return final

@router.delete("/deleteproduct/{id}")
def product_delete(id:int,db:Session=Depends(get_db)):
    final=delete_product(id,db)
    return final



@router.patch("/updatemanufacturerprofile/{id}")
def update_profile_manufacturer(id,data:UpdateManufacturerProfleSchemas,db:Session=Depends(get_db)):
    final=profile_update_manufacturer(id,data,db)
    return final