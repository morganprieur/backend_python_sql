
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

    user = relationship('User', back_populates='department', 
        cascade='all, delete') 

    def __str__(self): 
        return f'Modèle Département : {self.name}, id : {self.id}.' 

    def __repr__(self): 
        return str(self) 
        # return f'User {self.__str__()}' 


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
    #TODO: password type ? 
    password = Column( 
        # Password, 
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
    token = Column( 
        String, 
        unique=True 
    ) 

    department = relationship('Department', back_populates='user') 
    clients = relationship("Client", back_populates="user", 
        cascade='all, delete') 
    # user = relationship('User', back_populates='department', 
    #     cascade='all, delete') 
    events = relationship("Event", back_populates="user") 
    # events = relationship("Event", back_populates="users", nullable=True)  # pas autorisé 

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
        unique=False, 
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
    contract = relationship("Contract", back_populates="client", 
        cascade='all, delete') 
    # contract = relationship("Contract", back_populates="clients") 

    def __str__(self): 
        return f'Modèle Client : {self.name}, id : {self.id}.' 

    def __repr__(self): 
        return str(self) 


class Contract(Base): 
    __tablename__ = 'contracts' 
    id = Column( 
        Integer, 
        primary_key=True, 
        unique=True, 
        index=True 
    ) 
    client_id = Column( 
        Integer, 
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

    client = relationship("Client", back_populates="contract") 
    # clients = relationship("Client", back_populates="contract") 
    events = relationship("Event", back_populates="contracts", 
        cascade='all, delete') 

    def __str__(self): 
        return f'Modèle Contract : id {self.id}, client id : {self.client_id}.' 

    def __repr__(self): 
        return str(self) 


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
        unique=False, 
        index=True 
    ) 
    contract_id = Column( 
        Integer, 
        ForeignKey('contracts.id'), 
        unique=True, 
    ) 
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
    attendees = Column( 
        Integer 
    ) 
    notes = Column( 
        String 
    ) 

    user = relationship("User", back_populates="events") 
    # support_contact = relationship("User", back_populates="events") 
    contracts = relationship("Contract", back_populates="events") 

    def __str__(self): 
        return f'Modèle événement : {self.name}, id : {self.id}.' 

    def __repr__(self): 
        return str(self) 






