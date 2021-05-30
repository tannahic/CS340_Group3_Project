
from flask import Flask, render_template, json, request, redirect
import os
import CS340_Group3_Project.database.db_connector as db
from CS340_Group3_Project.support import *

app = Flask(__name__)

db_connection = db.connect_to_database()


# routes to pages
# home page
@app.route('/')
def index():
    return render_template("index.j2")


@app.route('/update', methods=['POST'])
def update_page():
    # convert form data to dictionary
    dict1 = request.form.to_dict()
    print(dict1)
    table = dict1['table']
    print(table)
    id_value = dict1[list(dict1)[1]]
    print(id_value)
    my_id = table[:-1] + '_id'
    print(my_id)
    formfill_query = "SELECT * FROM "  + table +  " WHERE " + my_id + " = " + id_value + ";"
    print(formfill_query)
    cursor = db.execute_query(db_connection=db_connection, query=formfill_query)
    result = cursor.fetchall()
    cursor.close()
    page = '/' + table
    return render_template("update.j2", clients=result )


# delete button input post route for veterinarian deletion
@app.route('/delete', methods=['POST'])
def delete():
    # convert form data to dictionary
    dict1 = request.form.to_dict()
    print(dict1)
    delete_query = "DELETE FROM veterinarians WHERE vet_id = " + '\'' + dict1['vet_id'] + '\';'
    cursor = db.execute_query(db_connection=db_connection, query=delete_query)
    db_connection.commit()
    cursor.close()
    page = '/veterinarians'
    return redirect(page)


# delete button input post route for vet_patient deletion
@app.route('/delete_vp', methods=['POST'])
def delete_vp():
    # convert form data to dictionary
    dict1 = request.form.to_dict()
    delete_query = "DELETE FROM veterinarians_patients WHERE vet_id = " + '\'' + dict1['vet_id'] + '\' AND patient_id = '+ '\'' + dict1['patient_id'] + '\';'
    print(delete_query)
    cursor = db.execute_query(db_connection=db_connection, query=delete_query)
    db_connection.commit()
    cursor.close()
    page = '/veterinarians_patients'
    return redirect(page)


# form input POST route for db insertion
@app.route('/insert', methods=['POST'])
def insert():

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
    # Write query to retrieve all columns
    query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth," \
            " CONCAT_WS(' ', first_name, last_name) AS client from patients LEFT JOIN clients" \
            " ON patients.client_id=clients.client_id;"
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
    parameter = 0
    # build search query
    search_query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth, CONCAT_WS(' ', first_name, last_name) AS client from patients LEFT JOIN clients ON patients.client_id=clients.client_id WHERE "
    # add data from dict1 to search query
    for i in dict1:
        
        if dict1[i] != "":
            search_query = search_query + i + ' = ' + '\'' + dict1[i] + '\' AND '
            parameter = parameter + 1
    # clean up query
    if parameter > 0:
        search_query = search_query[:-4]
    else:
        search_query = search_query + '0'
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
    query = "SELECT veterinarians_patients.vet_id, CONCAT('Dr. ', vet_last_name) as Veterinarian, veterinarians_patients.patient_id, CONCAT_WS(' ', patient_name, last_name) from veterinarians_patients LEFT JOIN veterinarians ON veterinarians_patients.vet_id = veterinarians.vet_id LEFT JOIN patients ON veterinarians_patients.patient_id = patients.patient_id LEFT JOIN clients on patients.client_id = clients.client_id;"

    cursor = db.execute_query(db_connection=db_connection, query=query)

    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    vet_list = get_vet_dropdown()
    patient_list = get_patient_dropdown()
    # Sends the results back to the web browser.
    return render_template("vets_patients.j2", veterinarians_patients=result, dropdown1=vet_list, dropdown2=patient_list)


# Start app
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 1994))
    app.run()
    # (host='0.0.0.0', port=port, debug=True)
