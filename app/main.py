from fastapi import FastAPI
from . import models
from app.database import engine




app = FastAPI()


models.Base.metadata.create_all(bind=engine)# create tbls for us 

@app.get("/")
def read_root():
    return {"message": "fast-coach-api"}