from fastapi import APIRouter,Depends,Query
from schemas.coustomer import CoustomerRegisterSchemas,CoustomerLogin,ChangePasswordSchemas,OtpSentSchemas,ResetPasswordSchemas,ProfileSchemas,WishlistSchemas,AddtoCartSchemas,OderSchemas,OrderCencelSchemas
from sqlalchemy.orm import Session
from utils.maindata import get_db
from controller.coustomer import coustomer_register,coustomer_login,change_password,sent_opt,reset_password,get_product,category_get,brand_get,create_profile,get_profile,wishlist_product,add_to_cart,create_order,cancel_order,get_all_order,delete_coustomer


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

@router.post("/wishlist")
def wishlist_create(data:WishlistSchemas,db:Session=Depends(get_db)):
    final=wishlist_product(data,db)
    return final


@router.post("/addtocart")
def add_cart(data:AddtoCartSchemas,db:Session=Depends(get_db)):
    final=add_to_cart(data,db)
    return final

@router.post("/ordercreate")
def order_create(data:OderSchemas,db:Session=Depends(get_db)):
    final=create_order(data,db)
    return final


# @router.patch("/xyzxyz/{id}")
# def xyz_xyz(id:int,db:Session=Depends(get_db)):
#     final=xyz(id,db)
#     return final


@router.delete("/cencelorder")
def oder_cencel(data:OrderCencelSchemas,db:Session=Depends(get_db)):
    final=cancel_order(data,db)
    return final

@router.get("/getallorder/{id}")
def all_order_get(id:int,db:Session=Depends(get_db)):
    final=get_all_order(id,db)
    return final

@router.delete("/deletecoustomer/{id}")
def coustomer_delete(id:int,db:Session=Depends(get_db)):
    final=delete_coustomer(id,db)
    return final
