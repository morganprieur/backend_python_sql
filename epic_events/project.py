
from sqlalchemy import create_engine 
import psycopg2 
from models import Base, Department  
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
    conn = engine.connect() 
    # print(conn) 
    print('success!') 

    Base.metadata.drop_all(bind=conn) 
    Base.metadata.create_all(bind=conn) 

    Session = sessionmaker(bind=conn) 
    session = Session() 

    vente = Department(name='vente') 
    session.add(vente) 
    session.commit() 

    vente_db = session.query(Department).filter(Department.name == 'vente').first() 
    print(f'produit trouvé : {vente_db.name}, id : {vente_db.id}.') 

    conn.commit() 

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