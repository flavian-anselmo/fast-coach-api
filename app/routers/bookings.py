'''
all endpoints regarding booking of a bus 


get req 
-----------
1. get bookings by status upcoming -- past etc 

2. bookigns are fteched according to logged in user 


'''


from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2



router = APIRouter(
  
    prefix = '/ticket',
    tags = ['Book a ticket ']
)



@router.post('/book', status_code=status.HTTP_201_CREATED)
async def book_ticket(ticket:schemas.BookTicketCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    book a ticket 

    '''
    new_ticket = models.BookTicket(**ticket.dict())
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return {'message':'Ticket Booked Successfully'}


@router.get('/book', response_model=List[schemas.BookTicketResponse])
async def get_ticket_booked(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    only the login user will be able to get a ticket 

    '''
    ticket = db.query(models.BookTicket).filter(models.BookTicket.passenger_id == curr_user.user_id).all()
    if not ticket:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='ticket not found')
    return ticket    
    

    
@router.get('/bus', response_model=List[schemas.BusResponse])
async def get_bus_routes(leaving_from:str, going_to:str, db:session =  Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get a bus to book with specific filter with travel location 

    - leaving_from 
    - going_to 

    '''
    bus_routes_join = db.query(models.Bus).join(models.TravelRoute, models.Bus.route_id == models.TravelRoute.route_id, isouter = True)
    bus_routes =  bus_routes_join.filter(models.TravelRoute.going_to.__eq__(going_to) and models.TravelRoute.leaving_from.__eq__(leaving_from)).all()
    if not bus_routes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='currently are not operatng in those routes')
    return bus_routes

