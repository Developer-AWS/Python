import psycopg2
from psycopg2 import Error
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    connection = psycopg2.connect(user = "USER",
                                  password = "PASS",
                                  host = "ENDPOINT",
                                  port = "5432",
                                  database = "postgres")
    
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    
    dropdatabse_smart = '''DROP DATABASE IF EXISTS  smartfreightvariablesdev;'''
    
    cursor.execute(dropdatabse_smart)
    connection.commit()
    print("Delete table successfully in PostgreSQL ")
#    time.sleep(5) 

    create_database_query = '''CREATE DATABASE smartfreightvariablesdev; '''
    
    cursor.execute(create_database_query)
    connection.commit()
    print("Database created successfully in PostgreSQL ")
#    time.sleep(3)

    os.system("export PGPASSWORD='PASS'; psql -h ENDPOINT -p 5432 -U USER -d smartfreightvariablesdev < smartfreightvariables_hml.sql")

except (Exception, psycopg2.DatabaseError) as error :
    print ("Error while creating PostgreSQL table", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

