from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2

router = APIRouter(
  
    prefix = '/payments',
    tags = ['payments']
)

@router.post('/stkpush')
async def pay_for_ticket(db:session = Depends(get_db)):
    '''
    will make payment to daraja api 

    '''
    pass 

