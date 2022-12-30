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
        pass
    def send_sms(self):
        '''
        send a text after a booking is done successfully and also when the travel date approaches 
        
        '''
        pass 

if __name__ == '__main__':
    PaymentService().checkout()

