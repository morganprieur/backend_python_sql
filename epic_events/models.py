
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean 
from sqlalchemy.orm import relationship, declarative_base 

import os 
import bcrypt 

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

    user = relationship('User', back_populates='department') 

    def __str__(self): 
        return f'Modèle Département : {self.name}, id : {self.id}.' 

    def __repr__(self): 
        return str(self) 
        # return f'User {self.__str__()}' 

    # def select_one_item(self, itemName, value): 
    #     # print('dept attribute L34 : ', attribute) 
    #     itemName = self.session.query(Department).filter(Department.name==value).first() 
    #     return itemName 
    #     # return self.repr() 


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
    #TODO: password_hash 
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
        ForeignKey('departments.id'), 
    ) 

    department = relationship('Department', back_populates='user') 
    clients = relationship("Client", back_populates="user") 
    events = relationship("Event", back_populates="user") 

    def __str__(self): 
        return f'Modèle User : {self.name}, id : {self.id}.' 

    def __repr__(self): 
        return str(self) 
        # return f'User {self.name}' 


class Client(Base): 
    __tablename__ = 'clients' 

    id = Column( 
        Integer, 
        primary_key=True, 
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
        ForeignKey("users.id"), 
    ) 

    user = relationship('User', back_populates="clients") 
    contract = relationship("Contract", back_populates="clients") 

    def __str__(self): 
        return f'Modèle Client : {self.name}, id : {self.id}.' 

    def __repr__(self): 
        return str(self) 
        # return f'Client {self.name}' 

    def add_item(self, itemName, fields:list): 
        itemName = Client( 
            name=fields[0], 
            email=fields[1], 
            phone=fields[2], 
            corporation_name=fields[3], 
            created_at=fields[4], 
            updated_at=fields[5], 
            sales_contact_id=fields[6], 
        ) 
        return itemName 


class Contract(Base): 
    __tablename__ = 'contracts' 
    id = Column( 
        Integer, 
        primary_key=True, 
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

    clients = relationship("Client", back_populates="contract") 
    events = relationship("Event", back_populates="contracts") 

    def __repr__(self): 
        return f'Contract {self.id}, client {self.client_id}' 


class Event(Base): 
    __tablename__ = 'events' 

    id = Column( 
        Integer, 
        primary_key=True, 
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
        ForeignKey('users.id'), 
        nullable=True 
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

    user = relationship("User", back_populates="events") 
    # support_contact = relationship("User", back_populates="events") 
    contracts = relationship("Contract", back_populates="events") 

    def __repr__(self): 
        return f'Event {self.name}' 






