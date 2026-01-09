from sqlalchemy import create_engine
from sqlalchemy.orm import Session,sessionmaker,declarative_base
from env.private_data import DATABASE_URL


engine=create_engine(DATABASE_URL,echo=True)
sessionlocal=sessionmaker(bind=engine,autoflush=False,autocommit=False)
Base=declarative_base()


def get_db():
    db:Session=sessionlocal()
    try:
        yield db
    finally:
        db.close()    



