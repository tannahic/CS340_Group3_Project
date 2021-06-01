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

def get_clinics_table():
    # query to retrieve all columns from clinics table
    select_query = "SELECT * FROM clinics;"
    cursor = db.execute_query(db_connection=db_connection, query=select_query)
    # retrieve all results to display in table
    clinics_table = cursor.fetchall()
    cursor.close()
    return clinics_table


def get_veterinarians_table():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT  vet_id, vet_first_name, vet_last_name, direct_phone, specialty, employment_status, vet_email," \
            " clinic_name FROM veterinarians LEFT JOIN clinics ON veterinarians.clinic_id=clinics.clinic_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    vets_table = cursor.fetchall()
    cursor.close()
    return vets_table


def get_clients_table():
    # query to retrieve all columns from clients table
    select_query = "SELECT * FROM clients;"
    cursor = db.execute_query(db_connection=db_connection, query=select_query)
    # return all results to display in table
    clients_table = cursor.fetchall()
    cursor.close()
    return clients_table


def get_patients_table():
    # s
    query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth," \
            " CONCAT_WS(' ', first_name, last_name) AS client from patients LEFT JOIN clients" \
            " ON patients.client_id=clients.client_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    # return all results to display in table
    patient_table = cursor.fetchall()
    cursor.close()
    return patient_table


def get_appointments_table():
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


def get_vets_patients_table():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT veterinarians_patients.vet_id, CONCAT('Dr. ', vet_last_name) as Veterinarian," \
            " veterinarians_patients.patient_id, CONCAT_WS(' ', patient_name, last_name)" \
            " FROM veterinarians_patients" \
            " LEFT JOIN veterinarians" \
            " ON veterinarians_patients.vet_id = veterinarians.vet_id" \
            " LEFT JOIN patients" \
            " ON veterinarians_patients.patient_id = patients.patient_id " \
            "LEFT JOIN clients ON patients.client_id = clients.client_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    vp_table = cursor.fetchall()
    cursor.close()
    return vp_table


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


def generate_update_query(table, dict_in):
    id_key = list(dict_in.keys())[0]
    id_value = list(dict_in.values())[0]
    dict_in.pop(id_key)
    update_query = "UPDATE " + table + " SET "
    for i in dict_in:
        update_query = update_query + i + ' = '

        if dict_in[i] == "":
            dict_in[i] = 'NULL'
            update_query = update_query + dict_in[i] + ', '
        else:
            update_query = update_query + '\'' + dict_in[i] + '\', '

    data = (id_key, id_value)
    update_query = update_query[:-2] + (" WHERE %s = %s;" % data)
    cursor = db.execute_query(db_connection=db_connection, query=update_query)
    db_connection.commit()
    cursor.close()


def vet_in_relation(vet_id):
    data = (vet_id, vet_id)
    query = ("SELECT a.vet_id, vp.vet_id FROM appointments a JOIN veterinarians_patients vp"
             " WHERE a.vet_id= %s OR vp.vet_id = %s;" % data)

    cursor = db.execute_query(db_connection=db_connection, query=query)
    result = cursor.rowcount
    print(result)
    cursor.close
    return result



