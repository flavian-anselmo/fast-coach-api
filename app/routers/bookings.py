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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='unexpected errorr')
    

# ----[track seats]-------
async def track_seats(bus_id:int, seat_no:str,db:session, booked_seat_track):
    '''
    track the seats 

    Algorithm
    1. check if the bus_id exists 
        if yes: 
            update the seats 
        if no -> this is a new bus in the list:
            make a post req     

    '''
    bus = db.query(models.BookedSeats).filter(models.BookedSeats.bus_id == bus_id).first()
    if bus:
        # update seat 
        print('pass 1')
        bus.booked_seats.append(seat_no)
        print('pass 2')
        db.commit()
        db.refresh(bus)
        return {'MSG':'OK 200'}
    # make a post
    new_booked_seat_tracking = models.BookedSeats(**booked_seat_track.dict())
    db.add(new_booked_seat_tracking)
    db.commit()
    db.refresh(new_booked_seat_tracking)

    return {'detail':'seat updated'}


       
      

@router.post('/book', status_code=status.HTTP_201_CREATED)
async def book_ticket(ticket:schemas.BookTicketCreate, booked_seat_track:schemas.BookedSeatsCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    book a ticket 

    '''
    try:

        new_ticket = models.BookTicket(**ticket.dict())
        seat = db.query(models.Bus).filter(models.Bus.bus_id == ticket.bus_id).first()
        if seat.no_of_seats != None:
            db.add(new_ticket)
            db.commit()
            await reduce_no_seats(
                ticket.bus_id,
                db,
            )
            await track_seats(
                ticket.bus_id,
                ticket.seat_no,
                db,
                booked_seat_track = booked_seat_track
            )
            db.refresh(new_ticket)
            return {'message':'Ticket Booked Successfully'}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The bus is fully booked')    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))







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


# ------------------------------------------------------[SETA TRACKING]---------------------------------------------------------------------------------------------------------
