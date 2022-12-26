from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.sql.expression import text
from app.database import Base
from sqlalchemy.orm import relationship




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
    passenger_id = Column(Integer, ForeignKey('users_tbl.user_id', ondelete="CASCADE"), nullable = False)
    passenger = relationship("User")
    bus_id = Column(Integer, ForeignKey('bus_tbl.bus_id', ondelete='CASCADE'), nullable = False)
    bus = relationship('Bus')






class User(Base):
    '''
    users specifically passengers who will be travelling upon booking a ticket 

    '''
    __tablename__ = "users_tbl"

    user_id =  Column(Integer, primary_key = True, nullable = False)
    email = Column(String , nullable = False, unique =  True )
    password = Column(String, nullable = False)
    is_passenger = Column(Boolean, nullable = False, server_default = 'TRUE')
    is_driver = Column(Boolean, nullable = False, server_default = 'False')
    is_admin = Column(Boolean, nullable = False, server_default = 'False')
    created_at =  Column (TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))




class TravelRoute(Base):
    '''
    define a route for a specifific bus eg a specific bus travels from nairobi to mombasa 
    Admin capabilities 


    '''
    __tablename__ = "travel_route_tbl"
    route_id = Column(Integer, primary_key = True, nullable = False)
    leaving_from = Column(String, nullable = False)
    going_to = Column(String, nullable = False)
    price = Column(Float, nullable = False)
    user_id = Column(Integer, ForeignKey('users_tbl.user_id', ondelete='CASCADE'), nullable = False)
    user = relationship('User')
    


class Bus(Base):
    '''
    Admin at fast coach will be  registering new buses 

    '''
    __tablename__ = "bus_tbl"
    bus_id = Column(Integer, primary_key = True, nullable = False)
    bus_name = Column(String, nullable = False)
    no_of_seats = Column(Integer, nullable = False)
    seat_arrangement = Column(String, nullable = False)
    route_id = Column(Integer, ForeignKey('travel_route_tbl.route_id', ondelete="CASCADE"), nullable = False)
    route = relationship('TravelRoute')
    user_id = Column(Integer, ForeignKey('users_tbl.user_id', ondelete='CASCADE'), nullable = False)
    user = relationship('User')







class Depature(Base):
    __tablename__ ="depature_tbl"
    '''
    this is what is sent to the user displaying when a bus is leaving and the 
    route its taking 

    '''

    dep_id = Column(Integer, primary_key = True, nullable = False )
    seats_available = Column(Integer, nullable =  False)
    booked_seats = Column(Integer, nullable = True)
    






# class Payments(Base):
#     __tablename__ = "payments_tbl"
#     '''
#     payments 

#     '''
#     pass 



