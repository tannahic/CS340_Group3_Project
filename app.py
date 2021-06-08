from flask import Flask, render_template, request, redirect, flash
import database.db_connector as db
from support import *

app = Flask(__name__)

db_connection = db.connect_to_database()


# Routes to pages and functions
# home page
@app.route('/')
def index():
    return render_template("index.j2")


# Clinics page
@app.route('/clinics')
def clinics():
    # retrieve data for clinics table
    clinics_data = get_clinics_table()
    # Send the data to the web browser via template.
    return render_template("clinics.j2", clinics=clinics_data, states=state_dict )


# Veterinarians page
@app.route('/veterinarians')
def vets():
    vets_data = get_veterinarians_table()
    # retrieve dropdown list of all clinics
    dropdown = get_clinic_dropdown()
    # Send data to browser via template
    return render_template("vets.j2", vets=vets_data, dropdown=dropdown)


# Clients page
@app.route('/clients')
def clients():
    clients_data = get_clients_table()
    # Send data to browser via template
    return render_template("clients.j2", clients=clients_data, states=state_dict)

# Patients page
@app.route('/patients')
def patients():
    patient_data = get_patients_table()
    dropdown = get_client_dropdown()
    # Send data to browser via template.
    return render_template("patients.j2", patients=patient_data, dropdown=dropdown)

# Appointments page
@app.route('/appointments')
def appointments():
    appointments_data = get_appointments_table()
    patient_list = get_patient_dropdown()
    vet_list = get_vet_dropdown()
    # Send data to browser via template
    return render_template("appointments.j2", appointments=appointments_data,
                           dropdown1=patient_list, dropdown2=vet_list)

# Veterinarians-Patients page
@app.route('/veterinarians_patients')
def vets_patients():
    vp_table = get_vets_patients_table()
    vet_list = get_vet_dropdown()
    patient_list = get_patient_dropdown()
    # Send data to browser via template.
    return render_template("vets_patients.j2", veterinarians_patients=vp_table, dropdown1=vet_list,
                           dropdown2=patient_list)


@app.route('/update', methods=['POST'])
def update_page():
    dict1 = request.form.to_dict()
    table = dict1['table']
    id_value = dict1[list(dict1)[1]]
    id_name = table[:-1] + '_id'
    data = (table, id_name, id_value)
    formfill_query = ("SELECT * FROM %s WHERE %s = %s ;" % data)
    cursor = db.execute_query(db_connection=db_connection, query=formfill_query)
    result = cursor.fetchall()
    cursor.close()
    client_data = get_clients_table()
    return render_template("update.j2", form_data=result, clients=client_data, states=state_dict)


@app.route('/update_result', methods=['POST'])
def update_submit():
    dict1 = request.form.to_dict()
    table = list(dict1.values())[0]
    # get first dictionary key
    table_key = list(dict1.keys())[0]
    # use key to remove first dictionary entry
    dict1.pop(table_key)
    generate_update_query(table, dict1)
    page = '/' + table
    return redirect(page)


# delete post route for veterinarian deletion
@app.route('/delete', methods=['POST'])
def delete():
    # convert form data to dictionary
    dict1 = request.form.to_dict()
    entity_id = 'vet_id' if dict1['table'] == 'veterinarians' else 'clinic_id'
    if dict1['table'] == 'veterinarians' and vet_is_foreign_key(dict1['id']):
        error = "Veterinarians associated with Appointments or Veterinarians_Patients cannot be deleted."
        vet_data = get_veterinarians_table()
        dropdown = get_clinic_dropdown()
        return render_template('vets.j2', vets=vet_data, dropdown=dropdown, error=error)

    else:
        query_data = (dict1['table'], entity_id,  dict1['id'])
        delete_query = ("DELETE FROM %s WHERE %s =  %s ;" % query_data)
        print(delete_query)
        cursor = db.execute_query(db_connection=db_connection, query=delete_query)
        cursor.close()
        page = '/' + dict1['table']
        return redirect(page)


# delete button input post route for vet_patient deletion
@app.route('/delete_vp', methods=['POST'])
def delete_vp():
    # convert form data to dictionary
    dict1 = request.form.to_dict()
    delete_query = "DELETE FROM veterinarians_patients WHERE vet_id = " + '\'' + dict1['vet_id'] + \
                   '\' AND patient_id = ' + '\'' + dict1['patient_id'] + '\';'
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
    # get first dictionary key
    table_key = list(dict1.keys())[0]
    # use key to remove first dictionary entry
    dict1.pop(table_key)
    page = '/' + table
    if table == "veterinarians_patients" and vet_patient_exists(dict1['vet_id'], dict1['patient_id']):
        error = "That relationship already exists. Only unique relationships can be added."
        vp_table = get_vets_patients_table()
        vet_list = get_vet_dropdown()
        patient_list = get_patient_dropdown()
        # Send data to browser via template.
        return render_template("vets_patients.j2", veterinarians_patients=vp_table, dropdown1=vet_list,
                               dropdown2=patient_list, error=error)
    else:
        generate_insert_query(table, dict1)

    return redirect(page)


@app.route('/search')
def search_page():
    patients_data = get_patients_table()
    dropdown = get_client_dropdown()
    # send data to browser via template
    return render_template("search.j2", patients=patients_data, dropdown=dropdown)


@app.route('/search_result', methods=['POST'])
def search_result():
    # convert form data to dictionary
    dict1 = request.form.to_dict()
    parameter = 0
    # build search query
    search_query = "SELECT patient_id, patient_name, species, breed, color, sex, date_of_birth," \
                   " CONCAT_WS(' ', first_name, last_name) AS client from patients LEFT JOIN clients" \
                   " ON patients.client_id=clients.client_id WHERE "
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
    return render_template("search.j2", patients=result, dropdown=dropdown, id='FocusOnSearchResult()')


@app.route('/update_clinics', methods=['POST'])
def update_clinics_page():
    dict1 = request.form.to_dict()
    table = dict1['table']
    id_value = dict1[list(dict1)[1]]
    id_name = table[:-1] + '_id'
    data = (table, id_name, id_value)
    formfill_query = ("SELECT * FROM %s WHERE %s = %s ;" % data)
    cursor = db.execute_query(db_connection=db_connection, query=formfill_query)
    result = cursor.fetchall()
    cursor.close()
    clinic_data = get_clinics_table()
    return render_template("update_clinics.j2", form_data=result, clinics=clinic_data, states=state_dict)


# Start app
if __name__ == "__main__":
    # port = int(os.environ.get('PORT', 1994))
    app.run()
    # (host='0.0.0.0', port=port, debug=True)
