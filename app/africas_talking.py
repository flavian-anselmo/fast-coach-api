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

class PaymentService:
    def __init__(self) -> None:
        self.username = 'sandbox'
        self.api_key = '5385dfb553bd3ad9d181a3b87f04f5ee307ef84a776f294eeef34609b900a658'
        africastalking.initialize(username = self.username, api_key = self.api_key)
        self.payment = africastalking.Payment

    def checkout (self):
        '''
        pay for the product 

        '''
        productName:str = 'Fast.Coach.API'
        phoneNumber:str = '+254798071510'
        currencyCode:str = 'KES'
        amount = 10.50
        metadata = {"agentId" : "654", "productId" : "321"}

        try:
            res = self.payment.mobile_checkout(productName, phoneNumber, currencyCode, amount, metadata)
            print (res)
        except Exception as e:
            print ("Received error response:%s" %str(e))


class SMS:
    def __init__(self) -> None:
        self.username = 'sandbox'
        self.api_key = '5385dfb553bd3ad9d181a3b87f04f5ee307ef84a776f294eeef34609b900a658'
        africastalking.initialize(username = self.username, api_key = self.api_key)
        self.sms = africastalking.SMS
    async def send_sms(self, recipient:list[str], msg:str):
        '''
        send a text after a booking is done successfully and also when the travel date approaches 
        
        '''
        recipients = recipient
        message = msg
        sender = "1795"
        try:
            response = self.sms.send(message, recipients, sender)
            return response
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


if __name__ == '__main__':
    PaymentService().checkout()
    # SMS().send_sms()
