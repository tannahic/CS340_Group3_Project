
from flask import Flask, render_template, json
import os
import database.db_connector as db


app = Flask(__name__)

db_connection = db.connect_to_database()


# routes to pages
# home page
@app.route('/')
def index():
    return render_template("index.j2")

# Clinics page
@app.route('/clinics')
def clinics():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT * FROM clinics;"

    cursor = db.execute_query(db_connection=db_connection, query=query)

    # return all results to display in table
    result = cursor.fetchall()

    # Sends the results back to the web browser.
    return render_template("clinics.j2", clinics=result )

# Veterinarians page
@app.route('/vets')
def vets():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT  vet_id, vet_first_name, vet_last_name, direct_phone, specialty, employment_status, vet_email, clinic_id FROM veterinarians;"

    cursor = db.execute_query(db_connection=db_connection, query=query)

    # return all results to display in table
    result = cursor.fetchall()

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

    # Sends the results back to the web browser.
    return render_template("appointments.j2", appointments=result)

# Veterinarians-Patients page
@app.route('/vets_patients')
def vets_patients():
    # Write query to retrieve all columns and save to a variable
    query = "SELECT * FROM veterinarians_patients;"

    cursor = db.execute_query(db_connection=db_connection, query=query)

    # return all results to display in table
    result = cursor.fetchall()

    # Sends the results back to the web browser.
    return render_template("vets_patients.j2", veterinarians_patients=result)


# Start app
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 1993))
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(host='0.0.0.0', port=port, debug=False)
