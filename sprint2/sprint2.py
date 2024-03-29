import flask
from flask import jsonify
from flask import request 
from sql import create_connection
from sql import execute_read_query
from sql import execute_query
import creds
import hashlib
from flask import request, make_response

# setting up an application name
app = flask.Flask(__name__) # sets up the application
app.config["DEBUG"] = True # allow to show errors in browser

# setting up the login page 
# creating a list to store username and passwords
authorizedspaceman = [
    {
        # default user
        'username': 'Space',
        'password': 'Galaxy' 
    },
]


@app.route('/login', methods=['POST'])
def usernamepw_example():
    username = request.headers.get('username')
    password = request.headers.get('password')
    for user in authorizedspaceman:
        if user['username'] == username and user['password'] == password:
            return 'Login Successful'
    return 'LOGIN ERROR'

@app.route('/api/authorizedspaceman', methods=['GET'])
def get_authorizedspaceman():
    return jsonify(authorizedspaceman)





# GET API Captain - to view entire captain table 
@app.route('/api/captain/all') # Api to read all of the rows that ate in the captain table
def api_all_captains():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    view_captain= "SELECT * FROM captain"
    cap = execute_read_query(conn, view_captain)
    return jsonify(cap)

# POST API Captain - to add a captain 
@app.route('/api/captain', methods = ['POST']) # Adding new rows into the captain table 
def add_new_captain():
    request_data = request.get_json()
    newfn = request_data['firstname']
    newln = request_data['lastname']
    newrank = request_data['captain_rank']
    newcapsecID = request_data['sec_cap_id']
    newhomeplanet = request_data['homeplanet']


    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    
    insert_new_captain = "INSERT INTO captain(firstname, lastname, captain_rank, homeplanet, sec_cap_id) VALUES ('%s','%s','%s', '%s', %s)" % (newfn, newln, newrank, newhomeplanet, newcapsecID)
    execute_query(conn, insert_new_captain)

    return "New Captain Successfully Added to Captain Table"

# DELETE API Captain - to delete a captain by rank 
@app.route('/api/captain', methods=['DELETE']) #API to delete a captain given the requested rank
def delete_Captain():
    request_data = request.get_json()
    RanktoDelete = request_data['ranking']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    delete_captain = "DELETE FROM captain WHERE ranking = '%s'" % (RanktoDelete)
    execute_query(conn, delete_captain)
    return "Captain Deleted Successfully"

# PUT API Captain - to update a captain's information 
@app.route('/api/captain', methods = ['PUT']) #API to update the ranking of the captain by requesting for the secondary ID
def update_captain():
    request_data = request.get_json()
    capid = request_data['sec_cap_id'] # created an extra collumn in the captain table so that the user could call 
    RanktoUpdate = request_data['ranking'] # the row that needed to be updated 

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    update_captain = "UPDATE captain SET ranking='%s' WHERE sec_cap_id=%s " % (RanktoUpdate, capid)
    execute_query(conn, update_captain)

    return 'Captain Table Updated'

 # END OF CAPTAIN TABLE API's

 
# GET API Spaceship - to view entire spaceship table 
@app.route('/api/spaceship/all') # Api to read all of the rows that are in the spaceship table 
def api_all_spaceships():
    
    request_data = request.get_json()
    cargotoadd = request_data['weight']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    view_ship= "SELECT * FROM spaceship WHERE maxweight >= %s" % (cargotoadd)  # select where maxweight is greater than or equal to the maxweight
    ships = execute_read_query(conn, view_ship)
    return jsonify(ships) # Api to read all of the rows that are in the spaceship table 

# POST API Spaceship - to add a spaceship
@app.route('/api/spaceship', methods = ['POST']) # API to add new rows into the spaceship table
def add_new_spaceship():
    request_data = request.get_json()
    newmaxw = request_data['maxweight']
    newcapid =request_data['captainid']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    
    insert_new_spaceship = "INSERT INTO spaceship(maxweight, captainid) VALUES ('%s',%s)" % (newmaxw, newcapid)
    execute_query(conn, insert_new_spaceship) 

    return "New Spaceship Successfully Added to Spaceship Table"

# DELETE API Spaceship - to delete a spaceship 
@app.route('/api/spaceship', methods=['DELETE']) # delete spaceship by secondary id 
def delete_spaceship():
    request_data = request.get_json()
    idToDelete = request_data['sec_ship_id'] # create variable to delete spaceship with secondary id 

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    delete_ship = "DELETE FROM spaceship WHERE sec_ship_id = %s" % (idToDelete)
    execute_query(conn, delete_ship)
    return "Spaceship Deleted Successfully"

# PUT API Spaceship - to update a spaceship's max weight
@app.route('/api/spaceship', methods = ['PUT']) #API to update spaceship max weight 
def update_spaceship():
    request_data = request.get_json()
    maxweightToUpdate= request_data['maxweight'] # create variable to update maxweight  
    captain_id = request_data['captainid'] # create variable to update ship from foreign id key

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    update_ship = "UPDATE spaceship SET maxweight = %s WHERE captainid = %s " % (maxweightToUpdate,captain_id)
    execute_query(conn, update_ship)

    return 'Spaceship Table Updated'

# GET API Cargo - to view entire cargo table
@app.route('/api/cargo/all') # Api to read all of the rows that are in the cargo table 
def api_all_cargo():
    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    view_cargos= "SELECT * FROM cargo"
    cargo_all = execute_read_query(conn, view_cargos)
    return jsonify(cargo_all)

# POST API Cargo - to add a cargo
@app.route('/api/cargo', methods = ['POST']) # API to add new rows into the spaceship table
def add_new_cargo():
    request_data = request.get_json()
    new_weight = request_data['weight']
    new_cargotype =request_data['cargotype']
    ship_id = request_data['shipid']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    insert_new_cargo = "INSERT INTO cargo(weight, cargotype, shipid) VALUES (%s,'%s', %s) " % (new_weight, new_cargotype, ship_id)
    execute_query(conn, insert_new_cargo) 

# tried this loop for adding max number of cargos to ship but did not work
    # for insert_new_cargo in add_new_cargo:
    #     if insert_new_cargo[new_weight] < add_new_spaceship:
    #         sum = sum + insert_new_cargo

    return "New Cargo Successfully Added to Cargo Table"

# DELETE API Cargo - to delete a cargo 
@app.route('/api/cargo', methods=['DELETE']) # delete cargo by fk shipid
def delete_cargo():
    request_data = request.get_json()
    idToDelete = request_data['shipid'] # create variable to delete spaceship with fk shipid 

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    delete_cargo = "DELETE FROM cargo WHERE shipid = %s" % (idToDelete)
    execute_query(conn, delete_cargo)
    return "Cargo Deleted Successfully"

# PUT API Cargo - to update a cargo with depart and arrive dates
@app.route('/api/cargo', methods = ['PUT']) #API to update Cargo
def update_cargo():
    request_data = request.get_json()
    arriveToUpdate= request_data['arrival'] # create variable to update arrival date
    departToUpdate = request_data['departure'] # create variable to update departure date
    ship_id = request_data['shipid']

    myCreds = creds.Creds()
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    update_cargo = "UPDATE cargo SET arrival = %s, departure = %s WHERE shipid = %s " % (arriveToUpdate, departToUpdate, ship_id)
    execute_query(conn, update_cargo)

    return 'Cargo Table Updated'






app.run()
