
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean 
from sqlalchemy.orm import relationship, declarative_base 


Base = declarative_base() 


class Department(Base): 
    __tablename__ = 'departments' 
    id = Column( 
        Integer, 
        unique=True, 
        primary_key=True 
    ) 
    name = Column( 
        String, 
        unique=True 
    ) 

    user = relationship('User', back_populates='departments') 


class User(Base): 
    __tablename__ = 'users' 
    id = Column( 
        Integer, 
        primary_key=True, 
        index=True 
    ) 
    name = Column( 
        String, 
        unique=True, 
        index=True 
    ) 
    email = Column( 
        String, 
        unique=True, 
        index=True 
    ) 
    #TODO: password_hash + max_length 
    password = Column( 
        String, 
        unique=True, 
    ) 
    phone = Column( 
        String, 
        unique=True 
    ) 
    department_id = Column( 
        Integer, 
        ForeignKey('demartments.id'), 
    ) 

    department = relationship('Department', back_populates='users') 
    client = relationship("Client", back_populates="users") 
    event = relationship("User", back_populates="users") 

    def __repr__(self): 
        return f'User {self.name}' 

class Client(Base): 
    __tablename__ = 'clients' 

    id = Column( 
        Integer, 
        unique=True, 
        index=True 
    ) 
    name = Column( 
        String, 
        unique=True, 
        index=True 
    ) 
    email = Column( 
        String, 
        unique=True, 
        index=True 
    ) 
    phone = Column( 
        String, 
        unique=True, 
        index=True 
    ) 
    corporation_name = Column( 
        String, 
        unique=True, 
        index=True 
    ) 
    #TODO Auto *** 
    created_at = Column( 
        DateTime 
    ) 
    #TODO Auto *** 
    updated_at = Column( 
        DateTime 
    ) 
    sales_contact_id = Column( 
        Integer, 
        ForeignKey("user.id"), 
    ) 

    sales_contact = relationship('User', back_populates="clients") 
    contract = relationship("Contract", back_populates="clients") 

    def __repr__(self): 
        return f'Client {self.name}' 


class Contract(Base): 
    __tablename__ = 'contracts' 
    id = Column( 
        Integer, 
        unique=True, 
        index=True 
    ) 
    client_id = Column( 
        ForeignKey('clients.id') 
    ) 
    # A diviser par 100 pour retrouver un prix avec centimes 
    amount = Column( 
        Integer 
    ) 
    # A diviser par 100 pour retrouver un prix avec centimes 
    paid_amount = Column( 
        Integer 
    ) 
    is_signed = Column( 
        Boolean 
    ) 
    #TODO Auto *** 
    created_at = Column( 
        DateTime 
    ) 

    client = relationship("User", back_populates="contracts") 
    event = relationship("Event", back_populates="contracts") 

    def __repr__(self): 
        return f'Contract {self.id}, client {self.client_id}' 


class Event(Base): 
    __tablename__ = 'events' 

    id = Column( 
        Integer, 
        unique=True, 
        index=True 
    ) 
    name = Column( 
        String, 
        unique=True, 
        index=True 
    ) 
    contract_id = Column( 
        Integer, 
        ForeignKey('contracts.id') 
    ) 
    # client_contact = Column( 
    #     string 
    # ) 
    start_datetime = Column( 
        DateTime 
    ) 
    end_datetime = Column( 
        DateTime 
    ) 
    support_contact_id = Column( 
        Integer, 
        ForeignKey('users.id') 
    ) 
    location = Column( 
        String 
    ) 
    Attendees = Column( 
        Integer 
    ) 
    notes = Column( 
        String 
    ) 

    support_contact = relationship("User", back_populates="events") 
    contract = relationship("Contract", back_populates="events") 

    def __repr__(self): 
        return f'Event {self.name}' 






