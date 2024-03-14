
from sqlalchemy import create_engine 
# import sqlalchemy 
import psycopg2 

# ======== 
# DATABASES = {
#     'ENGINE': 'django.db.backends.postgresql',
#     'NAME': os.environ.get('POSTGRES_DB'),
#     'USER': os.environ.get('POSTGRES_USER'),
#     'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
#     'HOST': 'db',
#     'PORT': os.environ.get('DB_PORT'), 
# }
# ======== 

# db_user = "app_user" 
db_user = "postgres" 
db_password = "postgres" 
# db_password = "secretpassword" 
# db_host = "192.168.240.1" 
# db_host = "127.0.0.1" 
# db_host = "0.0.0.0" 
db_host = "localhost" 
# db_host = "db_data" 
# db_host = "postgres" 
# db_host = "p12_work-postgres-1" 
db_port = "5432" 
db_name = "app_db" 

# db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
# db_url = f"psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}" 
# db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
# db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
print(db_url) 
# postgresql+psycopg2://app_user:secretpassword@localhost:5432/app_db
# http://localhost:8080/?pgsql=postgres&username=app_user&db=app_db&ns=public
# ======== 
# conn_url = 'postgresql+psycopg2://yourUserDBName:yourUserDBPassword@yourDBDockerContainerName/yourDBName'
# ======== 

engine = create_engine(db_url) 
print(engine) 

try: 
    conn = engine.connect() 
    print(conn) 
    print('success!') 
except Exception as ex: 
    print(ex) 

if conn is not None: 
    conn.close() 
    print('connex closed') 

print('hello') 

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