
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
        return f'Département : {self.name} (id : {self.id}).' 

    def __repr__(self): 
        return str(self) 
        # return f'User {self.__str__()}' 

    def to_dict(self): 
        return { 
            'id': self.id,
            'name': self.name
        } 


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

    department = relationship('Department', back_populates='user') 
    clients = relationship("Client", back_populates="user", 
        cascade='all, delete') 
    events = relationship("Event", back_populates="user") 

    def __str__(self): 
        return f'User (id : {self.id}) : {self.name}, {self.email}, hash mot de passe : {self.password}, téléphone : {self.phone}, département {self.department_id} {self.department.name}.' 

    def __repr__(self): 
        return str(self) 
        # return f'User {self.name}'

    def to_dict(self): 
        return { 
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'phone': self.phone,
            'department_id': self.department_id,
            'token': self.token
        } 


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
        return f'Client : {self.name} (id : {self.id}), contacts : {self.email} {self.phone}, entreprise : {self.corporation_name}, créé le {self.created_at}, mis à jour le {self.updated_at}, contact commerce : {self.user.name} (id : {self.user.id}).' 

    def __repr__(self): 
        return str(self) 


    def to_dict(self): 
        return { 
            'id': self.id, 
            'name': self.name, 
            'email': self.email, 
            'phone': self.phone, 
            'corporation_name': self.corporation_name, 
            'created_at': self.created_at, 
            'updated_at': self.updated_at, 
            'sales_contact_id': self.sales_contact_id 
        } 



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
    events = relationship("Event", back_populates="contracts", 
        cascade='all, delete') 

    def __str__(self): 
        return f'Contract : id {self.id}, client id : {self.client_id}, montant payé : {self.paid_amount}, is_signed : {self.is_signed}.' 

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
    contracts = relationship("Contract", back_populates="events") 

    def __str__(self): 
        if not self.support_contact_id: 
            support_contact_id = '' 
        else: 
            support_contact_id = self.support_contact_id 
        return f'Evénement : {self.name} (id : {self.id}), contrat : {self.contract_id}, début : {self.start_datetime}, fin : {self.end_datetime}, contact support ID : {support_contact_id}, lieu : {self.location}, invités : {self.attendees}, notes : {self.notes}).' 
        # return f'Evénement : {self.name} (id : {self.id}), contrat : {self.contract_id}, début : {self.start_datetime}, fin : {self.end_datetime}, contact support {self.user.name} (ID : {support_contact_id}), lieu : {self.location}, invités : {self.attendees}, notes : {self.notes}).' 

    def __repr__(self): 
        return str(self) 

    def to_dict(self): 
        if not self.support_contact_id: 
            support_contact_id = '' 
        else: 
            support_contact_id = self.support_contact_id 
        return { 
            'id': self.name, 
            'name': self.name, 
            'contract_id': self.contract_id, 
            'start_datetime': self.start_datetime, 
            'end_datetime': self.end_datetime, 
            'support_contact_id': support_contact_id, 
            'location': self.location, 
            'attendees': self.attendees, 
            'notes': self.notes, 
        } 





