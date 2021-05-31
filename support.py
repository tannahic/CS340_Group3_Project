import os
import database.db_connector as db

db_connection = db.connect_to_database()

state_dict = {
    'AK': 'Alaska', 'AL': 'Alabama', 'AR': 'Arkansas', 'AZ': 'Arizona', 'CA': 'California', 'CO': 'Colorado',
    'CT': 'Connecticut', 'DC': 'District of Columbia', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'GU': 'Guam',
    'HI': 'Hawaii', 'IA': 'Iowa', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'KS': 'Kansas', 'KY': 'Kentucky',
    'LA': 'Louisiana', 'MA': 'Massachusetts', 'MD': 'Maryland', 'ME': 'Maine', 'MI': 'Michigan', 'MN': 'Minnesota',
    'MO': 'Missouri', 'MS': 'Mississippi', 'MT': 'Montana', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'NE': 'Nebraska', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NV': 'Nevada', 'NY': 'New York',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VA': 'Virginia', 'VT': 'Vermont',
    'WA': 'Washington', 'WI': 'Wisconsin', 'WV': 'West Virginia', 'WY': 'Wyoming'
}


def get_client_dropdown():
    # query to return list of clients ids and names
    query2 = "SELECT client_id, CONCAT_WS(' ', first_name, last_name) AS client from clients;"
    cursor = db.execute_query(db_connection=db_connection, query=query2)
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
    query2 = "SELECT patient_id, CONCAT_WS(' ', patient_name, last_name) AS patient from patients" \
             " LEFT JOIN clients ON patients.client_id = clients.client_id;"
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


def generate_appointments_table():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT appointment_id, appointments.patient_id, CONCAT_WS(' ', patient_name, last_name)" \
            " AS patient, appointments.vet_id, vet_last_name, appointment_type, appointment_date," \
            " start_time, end_time FROM appointments LEFT JOIN patients ON" \
            " appointments.patient_id=patients.patient_id LEFT JOIN clients ON" \
            " patients.client_id=clients.client_id LEFT JOIN veterinarians ON" \
            " appointments.vet_id=veterinarians.vet_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    appointment_table = cursor.fetchall()
    cursor.close()
    return appointment_table


def generate_update_query(table, dict_in):
    id_key = list(dict_in.keys())[0]
    id_value = list(dict_in.values())[0]
    dict_in.pop(id_key)
    update_query = "UPDATE " + table + ' SET '
    for i in dict_in:
        update_query = update_query + i + ' = '

        if dict_in[i] == "":
            dict_in[i] = 'NULL'
            update_query = update_query + dict_in[i] + ', '
        else:
            update_query = update_query + '\'' + dict_in[i] + '\', '

    update_query = update_query[:-2] + ' WHERE ' + id_key + ' = \'' + id_value + '\';'
    commit_to_database(update_query)


def commit_to_database(query):
    cursor = db.execute_query(db_connection=db_connection, query=query)
    db_connection.commit()
    cursor.close()
