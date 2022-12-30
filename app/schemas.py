from datetime import datetime
from typing import Optional
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
    first_name:Optional[str]
    last_name:Optional[str]
    phone_number:Optional[str]
    is_passenger:bool
    is_admin:bool
    


class UserResponse(BaseModel):
    user_id :int
    email: EmailStr
    is_passenger:bool
    is_driver:bool
    is_admin:bool
    created_at:datetime
    class Config:
        orm_mode = True



class TokenResponse(BaseModel):
    access_token:str
    type:str
    class Config:        
        orm_mode = True
    
class TokenPayLoad(BaseModel):

    user_id:int




class TravelRouteCreate(BaseModel):
    leaving_from: str
    going_to: str 
    price: float
    
class TravelRouteResponse(TravelRouteCreate):
    '''
    response when getting routes posted 
    inherits from original travel toute 

    '''
    route_id:int 

    class Config:
        orm_mode = True
  




class BusCreate(BaseModel):
    user_id:int 
    route_id: int
    bus_name: str
    no_of_seats: int 
    bus_capacity: int
    seat_arrangement: str


class BusResponse(BusCreate):
    '''
    travel route of the specific bus 
    
    '''
    bus_id:int 
    route_id:int 
    user_id:int 
    route: TravelRouteResponse
    user: UserResponse
    class Config:
        orm_mode = True





class BookTicketCreate(BaseModel):
    ticket_id:int
    passenger_id:int 
    bus_id: int  
    leaving_from: str
    going_to:str
    seat_no: str
    travel_type:str

class BookTicketResponse(BookTicketCreate):
    is_paid:bool
    travel_status:str
    bus: BusResponse
    passenger:UserResponse
    class Config:
        orm_mode = True





class PaymentCreate(BaseModel):
    ticket_id: int 
    amount:float
    is_payment_succesfull: bool

class PaymentResponse(PaymentCreate):

    user_id:int 


    class Config:
        orm_mode = True







class DriverCreate(BaseModel):
    bus_id:str
    first_name:str
    last_name:str
    phone_number:str


class DriverResponse(DriverCreate):
    bus: BusResponse
    class Config:
        orm_mode = True
