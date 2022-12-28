'''
all endpoints regarding booking of a bus 


get req 
-----------
1. get bookings by status upcoming -- past etc 

2. bookigns are fteched according to logged in user 


'''


from datetime import timedelta
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


async def reduce_no_seats(bus_id:int, db:session):
    ''' 
    reduce the number of seats 

    get the bus id to acess the exact bus 

    '''
    try:
        seat = db.query(models.Bus).filter(models.Bus.bus_id == bus_id).first()
        if seat.no_of_seats != None:

            # if the seats availability is not zero 
            seat.no_of_seats = seat.no_of_seats - 1
            db.commit()
            db.refresh(seat)
            return seat 
        return {'message':'The bus is fully booked'}    
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='unexpected error')
    




@router.post('/book', status_code=status.HTTP_201_CREATED)
async def book_ticket(ticket:schemas.BookTicketCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    book a ticket 

    '''
    try:
        new_ticket = models.BookTicket(**ticket.dict())
        print(ticket.bus_id)
        db.add(new_ticket)
        db.commit()
        await reduce_no_seats(
            ticket.bus_id,
            db,
        )
        db.refresh(new_ticket)
        return {'message':'Ticket Booked Successfully'}
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='unexpected error')







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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='routes not found')
    return bus_routes



