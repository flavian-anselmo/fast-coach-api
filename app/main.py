from fastapi import FastAPI
from . import models
from app.database import engine
from app.routers import users, auth, admin

models.Base.metadata.create_all(bind=engine)# create tbls for us 



app = FastAPI(

    title= "fast-coach-api",
    description=" description",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "fast-coach-api",
        "url": "https://github.com/flavian-anselmo/fast-coach-api",
        "email": "anselmo.flavian@cloudpro.club",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)



# routers 

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(admin.router)

# root 
@app.get("/")
def read_root():
    return {"message": "fast-coach-api"}