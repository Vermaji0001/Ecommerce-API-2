from fastapi import APIRouter,Depends,Query,UploadFile,Form,File
from schemas.coustomer import CoustomerRegisterSchemas,CoustomerLogin,ChangePasswordSchemas,OtpSentSchemas,ResetPasswordSchemas,ProfileSchemas,WishlistSchemas,AddtoCartSchemas,OderSchemas,OrderCencelSchemas,RateUsSchemas,UpdateProfleSchemas,GetProductByCategory,GetProductByBrand
from sqlalchemy.orm import Session
from utils.maindata import get_db
from controller.coustomer import coustomer_register,coustomer_login,change_password,sent_opt,reset_password,get_product,category_get,brand_get,create_profile,get_profile,wishlist_product,add_to_cart,create_order,cancel_order,get_all_order,delete_coustomer,kyc_detail,review_on_product,cencel_add_to_cart,profile_update,searching_product,get_product_by_category,get_product_by_brand,get_all_product


router=APIRouter()

# Cosutomer Register
@router.post("/coustomerregister")
def register_coustomer(data:CoustomerRegisterSchemas,db:Session=Depends(get_db)):
    final=coustomer_register(data,db)
    return final

# Coustomer Login
@router.get("/coustomerlogin")
def login_coustomer(data:CoustomerLogin,db:Session=Depends(get_db)):
    final=coustomer_login(data,db)
    return final


# Change Password
@router.patch("/changepassword")
def passowrd_change(data:ChangePasswordSchemas,db:Session=Depends(get_db)):
    final=change_password(data,db)
    return final

# Sent Otp
@router.post("/sentotp")
def otp_sent(data:OtpSentSchemas,db:Session=Depends(get_db)):
    final=sent_opt(data,db)
    return 


# ResetPassword
@router.patch("/resetpassword")
def password_reset(data:ResetPasswordSchemas,db:Session=Depends(get_db)):
    final=reset_password(data,db)
    return final


# Get Product
@router.get("/getproduct/{id}")
def product_searching(id:int,db:Session=Depends(get_db)):
    final=get_product(id,db)
    return final


 #Get Category
@router.get("/getcategory")
def get_category(db:Session=Depends(get_db)):
    final=category_get(db)
    return final


# Get Brand
@router.get("/getbrand")
def get_brand(db:Session=Depends(get_db)):
    final=brand_get(db)
    return final



# Profile
@router.post("/profile")
def profile_create(data:ProfileSchemas,db:Session=Depends(get_db)):
    final=create_profile(data,db)
    return final


# Get Profile
@router.get("/getprofile/{id}")
def profile_get_by_id(id:int,db:Session=Depends(get_db)):
    final=get_profile(id,db)
    return final


# Wishlist
@router.post("/wishlist")
def wishlist_create(data:WishlistSchemas,db:Session=Depends(get_db)):
    final=wishlist_product(data,db)
    return final

# AddtoCart
@router.post("/addtocart")
def add_cart(data:AddtoCartSchemas,db:Session=Depends(get_db)):
    final=add_to_cart(data,db)
    return final


# Order Create
@router.post("/ordercreate")
def order_create(data:OderSchemas,db:Session=Depends(get_db)):
    final=create_order(data,db)
    return final


# Cancel Order
@router.delete("/cencelorder")
def oder_cencel(data:OrderCencelSchemas,db:Session=Depends(get_db)):
    final=cancel_order(data,db)
    return final


# Get All Order
@router.get("/getallorder/{id}")
def all_order_get(id:int,db:Session=Depends(get_db)):
    final=get_all_order(id,db)
    return final


# Delete Coustomer
@router.delete("/deletecoustomer/{id}")
def coustomer_delete(id:int,db:Session=Depends(get_db)):
    final=delete_coustomer(id,db)
    return final


# KYC
@router.post("/kyc")
async def details_kyc(coustomer_id:int=Form(...),
                document_image:UploadFile=File(...),
                account_holder_name:str=Form(...),
                account_number:int=Form(...),
                confirm_acc_number:int=Form(...),
                ifsc_code:str=Form(...),db:Session=Depends(get_db)):
    final= await kyc_detail(coustomer_id,document_image,account_holder_name,account_number,confirm_acc_number,ifsc_code,db)
    return final


# rate Us
@router.post("/rateus")
def reviews_submit(data:RateUsSchemas,db:Session=Depends(get_db)):
    final=review_on_product(data,db)
    return final


 #Delete ADD to Cart
@router.delete("/deleteaddtocart/{id}")
def addtocart_delete(id:int,db:Session=Depends(get_db)):
    final=cencel_add_to_cart(id,db)
    return final

 # Update Profile
@router.patch("/updateprofile/{id}")
def update_profile(id,data:UpdateProfleSchemas,db:Session=Depends(get_db)):
    final=profile_update(id,data,db)
    return final


#searching product 
@router.get("/xyzaa")
def product_searching(page:int=Query(1,ge=1),limit:int=Query(1,ge=1),name:str|None=None,db:Session=Depends(get_db)):
    final=searching_product(page,limit,name,db)
    return final

# get product by category  
@router.get("/getbycategory")
def product_get_by_category(data:GetProductByCategory,db:Session=Depends(get_db)):
    final=get_product_by_category(data,db)
    return final



# get product by brand    
@router.get("/getbybrand")
def product_get_by_brand(data:GetProductByBrand,db:Session=Depends(get_db)):
    final=get_product_by_brand(data,db)
    return final

#get all product

@router.get("/getallproduct")
def all_product_get(db:Session=Depends(get_db)):
    final=get_all_product(db)
    return final

