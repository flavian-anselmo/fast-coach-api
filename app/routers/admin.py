'''
all admin endpoints will be handled here

- setting up the routee table for the busses 
- registering new busses to the system 

'''


from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2


router = APIRouter(
  
    prefix = '/admin',
    tags = ['Admin endpoints']
)

@router.post('/routes', status_code = status.HTTP_201_CREATED, response_model=schemas.TravelRouteCreate)
async def create_bus_route(route:schemas.TravelRouteCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    admin will be adding bus routes 

    '''
    new_route = models.TravelRoute(**route.dict())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route


@router.post('/buses', status_code=status.HTTP_201_CREATED, response_model=schemas.BusCreate)
async def create_bus (bus:schemas.BusCreate,db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    create a new bus 
    '''
    new_bus = models.TravelRoute(**bus.dict())
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus
