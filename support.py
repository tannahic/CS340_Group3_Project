import os
import database.db_connector as db

db_connection = db.connect_to_database()


def get_client_dropdown():
    # query to return list of clients ids and names
    query2 = "SELECT client_id, CONCAT_WS(' ', first_name, last_name) AS client from clients;"
    # query the db
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    # store retrieved values in client_dropdown variable
    client_dropdown = cursor.fetchall()
    cursor.close()
    return client_dropdown

	
def get_clinic_dropdown():
    # query to return list of clinic ids and names
    query2 = "SELECT clinic_id, clinic_name FROM clinics;"
    # query the db
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    # store retrieved values in clinic_dropdown variable
    clinic_dropdown = cursor.fetchall()
    cursor.close()
    return clinic_dropdown
	
def get_patient_dropdown():
    # query to return list of patient ids and names
    query2 = "SELECT patient_id, CONCAT_WS(' ', patient_name, last_name) AS patient from patients LEFT JOIN clients ON patients.client_id = clients.client_id;"
    # query the db
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    # store retrieved values in patient_dropdown variable
    patient_dropdown = cursor.fetchall()
    cursor.close()
    return patient_dropdown
	
def get_vet_dropdown():
    # query to return list of vet ids and last names
    query2 = "SELECT vet_id, vet_last_name FROM veterinarians;"
    # query the db
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    # store retrieved values in vet_dropdown variable
    vet_dropdown = cursor.fetchall()
    cursor.close()
    return vet_dropdown