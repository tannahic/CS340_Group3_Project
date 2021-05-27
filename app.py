
from flask import Flask, render_template, json, request, redirect
import os
import database.db_connector as db
from support import *

app = Flask(__name__)

db_connection = db.connect_to_database()



# routes to pages
# home page
@app.route('/')
def index():
    return render_template("index.j2")


# form input POST route for db insertion
@app.route('/insert', methods=['POST'])
def insert():
    # convert form data to dictionary
    dict1 = request.form.to_dict()

    # get first value from dictionary (which is db table name)
    table = list(dict1.values())[0]
    # begin constructing INSERT query in 2 pieces
    insert_query = "INSERT INTO " + table + " ("
    values = "VALUES ("

    # get first dictionary key
    table_key = list(dict1.keys())[0]
    # use key to remove first dictionary entry
    dict1.pop(table_key)

    # use remaining dictionary entries to construct query
    for i in dict1:
        # key values are column names
        insert_query = insert_query + i + ', '
        # value strings are data to be inserted
        if dict1[i] == "":
            dict1[i] = 'NULL'
            values = values + dict1[i] + ', '
        else:
            values = values + '\'' + dict1[i] + '\', '

    # clean up strings and concatenate for final query
    insert_query = insert_query[:-2]
    insert_query = insert_query + ') '
    values = values[:-2] + ');'
    insert_query = insert_query + values + ';'

    cursor = db.execute_query(db_connection=db_connection, query=insert_query)
    db_connection.commit()
    cursor.close()
    page = '/' + table
    return redirect(page)


@app.route('/search')
def search_page():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth, CONCAT_WS(' ', first_name, last_name) AS client from patients LEFT JOIN clients ON patients.client_id=clients.client_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    query2 = "SELECT client_id, CONCAT_WS(' ', first_name, last_name) AS client from clients;"
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    dropdown = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("search.j2", patients=result, dropdown=dropdown)


@app.route('/search_result', methods=['POST'])
def search_result():
    # convert form data to dictionary
    dict1 = request.form.to_dict()
	
    # build search query
    search_query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth, CONCAT_WS(' ', first_name, last_name) AS client from patients LEFT JOIN clients ON patients.client_id=clients.client_id WHERE "
    # add data from dict1 to search query
    for i in dict1:
        print('%s %s', i, dict1[i])
        if dict1[i] != "":
            search_query = search_query + i + ' = ' + '\'' + dict1[i] + '\' AND '
    # clean up query
    search_query = search_query[:-4]
    search_query = search_query + ';'    
    cursor = db.execute_query(db_connection=db_connection, query=search_query)
    result = cursor.fetchall()
    cursor.close()
	
    dropdown = get_client_dropdown()
	
    return render_template("search.j2", patients=result, dropdown=dropdown)


# Clinics page
@app.route('/clinics')
def clinics():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT * FROM clinics;"

    cursor = db.execute_query(db_connection=db_connection, query=query)

    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("clinics.j2", clinics=result )

# Veterinarians page
@app.route('/veterinarians')
def vets():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT  vet_id, vet_first_name, vet_last_name, direct_phone, specialty, employment_status, vet_email, clinic_name FROM veterinarians LEFT JOIN clinics ON veterinarians.clinic_id=clinics.clinic_id;"

    cursor = db.execute_query(db_connection=db_connection, query=query)
    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    query2 = "SELECT clinic_id, clinic_name FROM clinics;"
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    dropdown = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("vets.j2", vets=result, dropdown=dropdown )

# Clients page
@app.route('/clients')
def clients():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT * FROM clients;"

    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("clients.j2", clients=result)

# Patients page
@app.route('/patients')
def patients():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth, CONCAT_WS(' ', first_name, last_name) AS client from patients LEFT JOIN clients ON patients.client_id=clients.client_id;"
    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    query2 = "SELECT client_id, CONCAT_WS(' ', first_name, last_name) AS client from clients;"
    cursor = db.execute_query(db_connection=db_connection, query=query2)
    dropdown = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("patients.j2", patients=result, dropdown=dropdown)

# Appointments page
@app.route('/appointments')
def appointments():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT appointment_id, appointments.patient_id, CONCAT_WS(' ', patient_name, last_name) AS patient, appointments.vet_id, vet_last_name, appointment_type, appointment_date, start_time, end_time FROM appointments LEFT JOIN patients ON appointments.patient_id=patients.patient_id LEFT JOIN clients ON patients.client_id=clients.client_id LEFT JOIN veterinarians ON appointments.vet_id=veterinarians.vet_id;"

    cursor = db.execute_query(db_connection=db_connection, query=query)
   
    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    patient_list = get_patient_dropdown()
    vet_list = get_vet_dropdown()
    # Sends the results back to the web browser.
    return render_template("appointments.j2", appointments=result, dropdown1=patient_list, dropdown2=vet_list)

# Veterinarians-Patients page
@app.route('/veterinarians_patients')
def vets_patients():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT * FROM veterinarians_patients;"

    cursor = db.execute_query(db_connection=db_connection, query=query)

    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("vets_patients.j2", veterinarians_patients=result)


# Start app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1994))
    app.run(host='0.0.0.0', port=port, debug=True)
