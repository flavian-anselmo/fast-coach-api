from datetime import datetime
from pydantic import BaseModel, EmailStr
class UserCreate(BaseModel):
    '''
    used with post req to create a user 
    {
        password: required 
        email: required
    }     

    '''
    email:EmailStr
    password:str 
    


class UserResponse(BaseModel):
    '''
    expected response once a user is created 

    '''
    user_id :int
    email: EmailStr
    password:str
    created_at:datetime
    class Config:
        orm_mode = True



