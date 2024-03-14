
# from sqlalchemy import create_engine 
import psycopg2 
# import sqlalchemy 

# db_user = "app_user" 
# db_password = "secretpassword" 
# # db_host = "localhost" 
# # db_host = "db_data" 
# # db_host = "P12_work-postgres" 
# db_host = "postgres" 
# db_port = "5432" 
# db_name = "app_db" 
# postgres

try: 
    conn = psycopg2.connect( 
        # database = "app_db", 
        user = "postgres", 
        # user = "app_user", 
        password = "postgres", 
        # password = "secretpassword", 
        host = "localhost", 
        # host = "0.0.0.0", 
        # db_host = "db_data" 
        # db_host = "P12_work-postgres" 
        # host = "postgres", 
        # port = "5432", 
        # dbname="nom_de_la_base_de_donnees",
        # user="nom_utilisateur",
        # password="mot_de_passe",
        # host="localhost",
        port="5432"
    ) 
    print(conn) 
    print('success') 
except Exception as ex: 
    print(ex) 

conn.close() 
print('connex closed') 

# db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}" 
# # db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}" 
# print(db_url) 
# # postgresql+psycopg2://app_user:secretpassword@localhost:5432/app_db
# # http://localhost:8080/?pgsql=postgres&username=app_user&db=app_db&ns=public
# # ======== 
# # conn_url = 'postgresql+psycopg2://yourUserDBName:yourUserDBPassword@yourDBDockerContainerName/yourDBName'
# # ======== 

# engine = create_engine(db_url) 

# # try: 
# conn = engine.connect() 
# print(conn) 
# print('success!') 
# # except Exception as ex: 
# #     print(ex) 


print('hello') 

if __name__ == "main": 
    main() 

