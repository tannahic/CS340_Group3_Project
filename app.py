
from flask import Flask, render_template, json, request, redirect
import os
import database.db_connector as db


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
    query = "SELECT  vet_id, vet_first_name, vet_last_name, direct_phone, specialty, employment_status, vet_email, clinic_id FROM veterinarians;"

    cursor = db.execute_query(db_connection=db_connection, query=query)

    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("vets.j2", vets=result)

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
    query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth, client_id FROM patients;"

    cursor = db.execute_query(db_connection=db_connection, query=query)
    
    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("patients.j2", patients=result)

# Appointments page
@app.route('/appointments')
def appointments():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT * FROM appointments;"

    cursor = db.execute_query(db_connection=db_connection, query=query)
   
    # return all results to display in table
    result = cursor.fetchall()
    cursor.close()
    # Sends the results back to the web browser.
    return render_template("appointments.j2", appointments=result)

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
