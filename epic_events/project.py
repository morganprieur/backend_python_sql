
from sqlalchemy import create_engine 
import psycopg2 
from models import Base, Client, Contract, Department, Event, User   
from sqlalchemy.orm import sessionmaker 

import os 

db_user = os.environ.get('POSTGRES_USER') 
db_password = os.environ.get("POSTGRES_PASSWORD") 
db_host = os.environ.get("POSTGRES_HOST") 
db_port = os.environ.get("DB_PORT") 
db_name = os.environ.get("POSTGRES_DB") 

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
# print(db_url) 

engine = create_engine(db_url) 
print(engine) 

try: 
    # conn = engine.connect() 
    # # print(conn) 
    # print('success!') 

    Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine) 

    Session = sessionmaker(bind=engine) 
    session = Session() 

    vente = Department(name='vente') 
    session.add(vente) 
    session.commit() 

    vente.name = 'commerce' 
    session.commit() 

    sales_user = User( 
        name='sales 1', 
        email='sales_1@mail.com', 
        password='S3cr3tp4ss', 
        phone='01 23 45 67 89', 
        department=vente 
    ) 
    session.add(sales_user) 
    session.commit() 

    vente_db = session.query(Department).filter(Department.id == 1).first() 
    print(f'département trouvé : {vente_db.name}, id : {vente_db.id}.') 

    users_db = session.query(User).filter(User.department==vente) 
    for user in users_db: 
        print(f'User trouvé : {user.name}, id : {user.id}, departement : {user.department.name}') 

    # conn.commit() 

except Exception as ex: 
    print(ex) 

print('hello') 


# if conn is not None: 
#     conn.close() 
#     print('connex closed') 


if __name__ == "main": 
    main() 



# ======== 
# def start():
#     engine = create_engine('sqlite:///:memory:')

#     Session = sessionmaker(bind=engine)
#     session = Session()

#     Base.metadata.create_all(engine)
#     return engine, session
# ======== 