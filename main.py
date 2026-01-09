from fastapi import FastAPI
from routes.coustomer import router as coustomer_router
from routes.manufacturer import router as manufacturer_router
from utils.maindata import engine,Base
from modals import all_modals


app=FastAPI()

app.include_router(coustomer_router)
app.include_router(manufacturer_router)


@app.on_event("startup")
def table_make():
    
    Base.metadata.create_all(bind=engine)

    
    
    