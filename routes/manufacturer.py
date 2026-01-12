from fastapi import APIRouter,Depends
from schemas.manufacturer import ManufactureRegisterSchemas,MnaufacturerLoginSchemas,ChangePasswordManufacturer,ManufacturerOtpSchemas,ResetPasswordManufacturer,ProfileManufacturerSchemas,UpdateManufacturerProfleSchemas,IncreaseQuantity,ProductCreateSchemas
from controller.manufacturer import manufacturer_register,manufacturer_login,product_create,change_password_manufacturer,sent_opt_manufacturer,reset_password_manufacturer,create_profile_manufacturer,get_profile_manufacturer,delete_manufacturer,delete_product,profile_update_manufacturer,increase_quantity
from sqlalchemy.orm  import Session
from utils.maindata import get_db


router=APIRouter()

# Manufacturer Register
@router.post("/manufacturerregister")
def register_manufacturer(data:ManufactureRegisterSchemas,db:Session=Depends(get_db)):
    final=manufacturer_register(data,db)
    return final

#manufacturer login
@router.get("/manufacturerlogin")
def login_manufacturer(data:MnaufacturerLoginSchemas,db:Session=Depends(get_db)):
    final=manufacturer_login(data,db)
    return final


#create product
@router.post("/createproduct")
def craete_product(data:ProductCreateSchemas,db:Session=Depends(get_db)):
    final= product_create(data,db)
    return final



#change Password
@router.patch("/changepasswordmanufacturer")
def manufacturer_change_password(data:ChangePasswordManufacturer,db:Session=Depends(get_db)):
    final=change_password_manufacturer(data,db)
    return final


#otp sent manufacturer
@router.post("/otpsentmanufacturer")
def manufacturer_otp_sent(data:ManufacturerOtpSchemas,db:Session=Depends(get_db)):
    final=sent_opt_manufacturer(data,db)
    return final


#reset password
@router.patch("/resetpassowrdmanufacturer")
def manufacturer_reset_password(data:ResetPasswordManufacturer,db:Session=Depends(get_db)):
    final=reset_password_manufacturer(data,db)
    return final

#manufacturer profile
@router.post("/manufacturerprofile")
def manufacturer_profile(data:ProfileManufacturerSchemas,db:Session=Depends(get_db)):
    final=create_profile_manufacturer(data,db)
    return final    

 #get profile
@router.get("/getmanufacturerprofile/{id}")
def get_manufacturer_profile(id:int,db:Session=Depends(get_db)):
     final=get_profile_manufacturer(id,db)
     return final


#delete manufacturer
@router.delete("/deletemanufacturer/{id}")
def manufacturer_delete(id:int,db:Session=Depends(get_db)):
    final=delete_manufacturer(id,db)
    return final

#delete product
@router.delete("/deleteproduct/{id}")
def product_delete(id:int,db:Session=Depends(get_db)):
    final=delete_product(id,db)
    return final


#update manufacturer
@router.patch("/updatemanufacturerprofile/{id}")
def update_profile_manufacturer(id,data:UpdateManufacturerProfleSchemas,db:Session=Depends(get_db)):
    final=profile_update_manufacturer(id,data,db)
    return final



@router.patch("/increaseproductquantity/{id}")
def product_quantity_increase(id:int,data:IncreaseQuantity,db:Session=Depends(get_db)):
    final=increase_quantity(id,data,db)
    return final
