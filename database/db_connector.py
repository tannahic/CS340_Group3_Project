import MySQLdb
import os
from dotenv import load_dotenv, find_dotenv
from database.db_credentials import dbCred

# Citation : This code is based heavily on the code presented in the CS340 flask-starter-app tutorial
# found at https://github.com/osu-cs340-ecampus/flask-starter-app


# Load our environment variables from the .env file in the root of our project.
# load_dotenv(find_dotenv())

# Set the variables in our application with those environment variables
# host = os.environ.get("340DBHOST")
# user = os.environ.get("340DBUSER")
# passwd = os.environ.get("340DBPW")
# db = os.environ.get("340DB")

def connect_to_database(host = dbCred.host, user = dbCred.user, passwd = dbCred.passwd, db = dbCred.db):
    
    db_connection = MySQLdb.connect(host,user,passwd,db)
    return db_connection

def execute_query(db_connection = None, query = None, query_params = ()):
   
	# check for database connection and re-establish if none
    db_connection.ping(True)

    if db_connection is None:
        print("No connection to the database found!")
        return None

    if query is None or len(query.strip()) == 0:
        print("No query found. Please pass a SQL query in query")
        return None

    print("Executing %s with %s" % (query, query_params));
    # Create a cursor to execute query. 
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
	#execute query
    cursor.execute(query, query_params)
    # if changes are made via query, they must be committed
    db_connection.commit();
    return cursor

# if __name__ == '__main__':
    
