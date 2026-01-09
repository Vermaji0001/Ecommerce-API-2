from fastapi import APIRouter,Depends,UploadFile,File,Form
from schemas.manufacturer import ManufactureRegisterSchemas,MnaufacturerLoginSchemas,ProductCreateSchemas
from controller.manufacturer import manufacturer_register,manufacturer_login,product_create
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
