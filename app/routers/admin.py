'''
all admin endpoints will be handled here

- setting up the routee table for the busses 
- registering new busses to the system 


TODO: GET ALL THE BUSES --> done 
TODO: GET ALL THE ROUTES  --> done 
TODO: GET SPECIFIC BUS WITH ITS ROUTE 
TODO: GET SPEPCIFIC ROUTE 
TODO: creat routes --> done 
TODO: CREATE BUSES --> done 



'''


from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2



router = APIRouter(
  
    prefix = '/admin',
    tags = ['Admin endpoints']
)





@router.post('/routes', status_code = status.HTTP_201_CREATED, response_model=schemas.TravelRouteResponse)
async def create_bus_route(route:schemas.TravelRouteCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''

    admin will be adding bus routes 

    '''
    new_route = models.TravelRoute(**route.dict())
    db.add(new_route)
    db.commit()
    db.refresh(new_route)
    return new_route




@router.get('/routes', response_model= List[schemas.TravelRouteResponse])
async def get_all_travel_routes(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all the travel routes 

    '''
    routes = db.query(models.TravelRoute).all()
    if not routes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus routes available')
    return routes    




@router.get('/routes/{route_id}', response_model=schemas.TravelRouteResponse)
async def get_route_by_id(route_id:int, curr_user:int = Depends(oauth2.get_current_user_logged_in), db:session = Depends(get_db)):
    '''
    get one route with id 
    '''
    route = db.query(models.TravelRoute).filter(models.TravelRoute.route_id == route_id ).first()

    if not route:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus route available')
    return route    



@router.delete('/routes/{route_id}')
async def delete_route(route_id:int, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    delete a travel route 

    '''
    bus = db.query(models.TravelRoute).filter(models.TravelRoute.route_id == route_id)
    bus.delete(synchronize_session = False)
    db.commit()    
    return {"detail": "deleted route sucessfully "}



@router.post('/buses', status_code=status.HTTP_201_CREATED, response_model=schemas.BusResponse)
async def create_bus (bus:schemas.BusCreate,db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    create a new bus 
    '''
    new_bus = models.Bus(**bus.dict())
    db.add(new_bus)
    db.commit()
    db.refresh(new_bus)
    return new_bus



@router.get('/buses', response_model=List[schemas.BusResponse])
async def get_all_buses(db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    get all the registered buses together with the route they take 

    '''
    buses  = db.query(models.TravelRoute).all()

    if not buses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus routes available')
    return buses   



@router.get('/buses/{bus_id}', response_model=schemas.BusResponse)
async def get_bus_by_id(bus_id:int, curr_user:int = Depends(oauth2.get_current_user_logged_in), db: session = Depends(get_db)):
    '''
    get one bus with routes 

    '''
    bus = db.query(models.Bus).filter(models.Bus.bus_id == bus_id ).first()

    if not bus:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='no bus route available')
    return bus  



@router.delete('/buses/{bus_id}')
async def delete_bus(bus_id:int, db: session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    delete  a registered bus 

    '''
    bus = db.query(models.Bus).filter(models.Bus.bus_id == bus_id)
    bus.delete(synchronize_session = False)
    db.commit()    
    return {"detail": "deleted bus sucessfully "}