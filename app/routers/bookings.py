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



@router.post('/book', status_code=status.HTTP_201_CREATED, response_model=schemas.TravelRouteResponse)
async def book_ticket(ticket:schemas.BookTicketCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    book a ticket 

    '''
    new_ticket = models.TravelRoute(**ticket.dict())
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket



async def get_ticket_booked():
    '''
    only the login user will be able to get a ticket 
    
    '''
    pass 

