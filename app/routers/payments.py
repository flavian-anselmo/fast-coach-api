from typing import List
from fastapi import APIRouter
from sqlalchemy.orm import session
from app.database import get_db
from fastapi import Depends, HTTPException, status
from app import models, schemas, oauth2
from sqlalchemy.exc import IntegrityError
from app.africas_talking import SMS
router = APIRouter(
  
    prefix = '/payments',
    tags = ['payments']
)



async def change_paid_status(db, ticket_id:int):
    '''
    change the paid status in booking table to paid 

    '''
    paid_status = db.query(models.BookTicket).filter(models.BookTicket.ticket_id == ticket_id).first()
    if paid_status.is_paid == False:
        # make the change 
        paid_status.is_paid = True
        db.commit()
        db.refresh(paid_status)
        if paid_status.is_paid:
            await notify_passenger_via_sms()
        return paid_status

async def notify_passenger_via_sms():
    '''
    after the user has paid notify them via sm 

    '''
    await SMS().send_sms(recipient=['+254798071510'], msg= 'Hello thanks for booking with fastcoach!')
    
    
    

@router.post('/stkpush', response_model=schemas.PaymentResponse)
async def pay_for_ticket(payament:schemas.PaymentCreate, db:session = Depends(get_db), curr_user:int = Depends(oauth2.get_current_user_logged_in)):
    '''
    initiate payment with africas talking stkpush  

    '''
    try:
        pay = models.Payments( **payament.dict(), user_id = curr_user.user_id)
        db.add(pay)
        db.commit()
        await change_paid_status(
            db,
            payament.ticket_id
        )
        db.refresh(pay)
        return pay
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))





