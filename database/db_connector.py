import MySQLdb
from database.db_credentials import dbCred

# Citation : This code is based heavily on the code presented in the CS340 flask-starter-app tutorial
# found at https://github.com/osu-cs340-ecampus/flask-starter-app, with modifications

# connects to database with credentials set in dbCred class
def connect_to_database(host=dbCred.host, user=dbCred.user, passwd=dbCred.password, db=dbCred.database):
    db_connection = MySQLdb.connect(host, user, passwd, db)
    return db_connection


def execute_query(db_connection=None, query=None, query_params=()):

    # check for database connection and re-establish if none
    db_connection.ping(True)

    # Error condition handling
    if db_connection is None:
        print("No connection to the database found!")
        return None

    if query is None or len(query.strip()) == 0:
        print("No query found. Please pass a SQL query in query")
        return None

    # logging statement to trace queries made
    print("Executing %s with %s" % (query, query_params))
    # Create a cursor to execute query. 
    cursor = db_connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, query_params)
    # commit changes made by query
    db_connection.commit()
    return cursor


