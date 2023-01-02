'''
configure payments with africas talking api 


parameters{
    username 
    productName 
    providerChanel 
    phoneNumber 
    currencyCode 
    amount
    metadata
}


5385dfb553bd3ad9d181a3b87f04f5ee307ef84a776f294eeef34609b900a658



'''

import africastalking
from fastapi import HTTPException, status
from app.config import settings

class PaymentService:
    def __init__(self) -> None:
        self.username = settings.africas_talking_env
        self.api_key = settings.africas_talking_api_key
        africastalking.initialize(username = self.username, api_key = self.api_key)
        self.payment = africastalking.Payment

    async def checkout (self, productName:str, phoneNumber:str, currencyCode:str, amount:float):
        '''
        pay for the product 

        '''
        # productName:str = 'Fast.Coach.API'
        # phoneNumber:str = '+254798071510'
        # currencyCode:str = 'KES'
        # amount = 10.50
        metadata = {"agentId" : "654", "productId" : "321"}

        try:
            res = self.payment.mobile_checkout(productName, phoneNumber, currencyCode, amount, metadata)
            return res
        except Exception as error:
            raise HTTPException(status_code = status.HTTP_417_EXPECTATION_FAILED, detail=str(error))


class SMS:
    def __init__(self) -> None:
        self.username = settings.africas_talking_env
        self.api_key = settings.africas_talking_api_key
        africastalking.initialize(username = self.username, api_key = self.api_key)
        self.sms = africastalking.SMS
    async def send_sms(self, recipient:list[str], msg:str):
        '''
        send a text after a booking is done successfully and also when the travel date approaches 
        
        '''
        # recipients = ['+254798071510']
        # message = 'hello'
        sender = settings.sender_code
        try:
            response =  self.sms.send(msg, recipient, sender)
            return response
        except Exception as error:
            raise HTTPException(status_code = status.HTTP_417_EXPECTATION_FAILED, detail=str(error))


def pay():
    PaymentService().checkout(
        'Fast.Coach.API',
        '+254798071510',
        'KES',
        10.50
    )

    SMS().send_sms(
        recipient = ['+254798071510'],
        msg = 'hello world',
    )



# pay()
