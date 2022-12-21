from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.sql.expression import text
from app.database import Base




class BookTicket(Base):
    '''
    defines the table where the user 
    will be booking travel 

    '''
    __tablename__ = "book_ticket_tbl"

    ticket_id = Column(Integer, primary_key = True, nullable = False)
    leaving_from = Column(String, nullable = False)
    going_to = Column(String, nullable = False)
    travel_status = Column(String, nullable = False, server_default = 'upcoming')
    travel_type = Column(String, nullable = False, server_default = 'oneway')
    is_paid = Column(Boolean, nullable = False, server_default = 'TRUE')
    seat_no = Column(String, nullable = False)
    # travel_date = Column(TIMESTAMP(timezone = True), nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))




class User(Base):
    '''
    users specifically passengers who will be travelling upon booking a ticket 

    '''
    __tablename__ = "users_tbl"

    user_id =  Column(Integer, primary_key = True, nullable = False)
    email = Column(String , nullable = False, unique =  True )
    password = Column(String, nullable = False)
    created_at =  Column (TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))





class Bus(Base):
    '''
    Admin at fast coach will be  registering new buses 

    '''
    __tablename__ = "bus_tbl"
    bus_id = Column(Integer, primary_key = True, nullable = False)
    bus_name = Column(String, nullable = False, unique = True)
    no_of_seats = Column(Integer, nullable = False)
    seat_arrangement = Column(String, nullable = False)




class TravelRoute(Base):
    '''
    define a route for a specifific bus eg a specific bus travels from nairobi to mombasa 
    

    '''
    __tablename__ = "travel_route_tbl"
    route_id = Column(Integer, primary_key = True, nullable = False)
    leaving_from = Column(String, nullable = False)
    going_to = Column(String, nullable = False)
    price = Column(Float, nullable = False)



class Depature(Base):
    '''
    this is what is sent to the user displaying when a bus is leaving and the 
    route its taking 

    '''


    pass 




class Payments(Base):
    '''
    payments 

    '''
    pass 



