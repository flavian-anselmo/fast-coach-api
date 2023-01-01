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



async def change_paid_status(db, ticket_id:int, curr_user_id:int):
    '''
    change the paid status in booking table to paid 

    '''
    try:
        paid_status = db.query(models.BookTicket).filter(models.BookTicket.ticket_id == ticket_id).first()
        if paid_status.is_paid == False:
            # make the change 
            paid_status.is_paid = True
            db.commit()
            db.refresh(paid_status)
            if paid_status.is_paid:
                await notify_passenger_via_sms(db, curr_user_id)
            return paid_status
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

async def notify_passenger_via_sms(db, curr_user_id:int):
    '''
    after the user has paid notify them via sm 

    '''
    try:
        user = db.query(models.User).filter(models.User.user_id == curr_user_id).first()
        if user:

            await SMS().send_sms(recipient=[user.phone_number], msg= f'Hello {user.last_name}, thanks for booking with fastcoach!')
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
        

async def payment_process_via_africans_talking():
    '''
    actual payment process 

    '''
    pass      
    

@router.post('/stkpush', response_model=schemas.PaymentResponse)
async def pay_for_ticket(payament:schemas.PaymentCreate, db:session = Depends(get_db), curr_user = Depends(oauth2.get_current_user_logged_in)):
    '''
    initiate payment with africas talking stkpush  

    '''
    try:
        pay = models.Payments( **payament.dict(), user_id = curr_user.user_id)
        db.add(pay)
        db.commit()
        await change_paid_status(
            db,
            payament.ticket_id,
            curr_user.user_id
        )
        db.refresh(pay)
        return pay
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error))





