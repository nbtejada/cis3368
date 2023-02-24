import flask
from flask import jsonify
from flask import request 
from sql import create_connection
from sql import execute_read_query
from sql import execute_query
import creds

#setting up an application name
app = flask.Flask(__name__) # sets up the application
app.config["DEBUG"] = True # allow to show errors in browser


# snowboard GET API - to see all snowboards
@app.route('/api/snowboard/all')
def api_all():             # define a function and name it accordingly
    myCreds = creds.Creds() # create mysql connection in the next 2 lines
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    select_boards = "SELECT * FROM snowboard"
    snowboard = execute_read_query(conn, select_boards)
    return jsonify(snowboard) 


# snowboard POST API - to add a snowboard
@app.route('/api/snowboard', methods = ['POST']) # method to load new data into the SQL Database
def add_snowboard():
    request_data = request.get_json() # statment for postman to work 
    newtype = request_data['boardtype'] # create new variable for inserting new boards
    newbrand = request_data['brand']
    newmsrp = request_data['msrp']
    newsize = request_data['size']

    myCreds = creds.Creds() # create my sql connection next 2 lines 
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)

    insert_board = "INSERT INTO snowboard(boardtype, brand, msrp, size) VALUES ('%s','%s', %s, %s)" % (newtype, newbrand, newmsrp, newsize)
    execute_query(conn, insert_board)

    return "Success"

#snowboard DELETE API - to delete a snowboard
@app.route('/api/snowboard', methods = ['DELETE']) 
def delete_snowboard():
    request_data = request.get_json() # statement for connection to postman
    idToDelete = request_data['id'] # deletes data based off id 
    
    myCreds = creds.Creds() # create my sql connection in the next 2 lines 
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    delete_board = 'DELETE FROM snowboard WHERE id = %s' % (idToDelete)
    execute_query(conn, delete_board)
    
    return 'Snowboard Deleted'

# snowboard PUT API - to update a snowboard's price
@app.route('/api/snowboard', methods = ['PUT'])
def update_snowboard():
    request_data = request.get_json()
    priceToUpdate = request_data['msrp'] # update price 
    idToSearch = request_data['id'] # update with corresponding id
    
    
    myCreds = creds.Creds() # create mysql connection in next 2 lines
    conn = create_connection(myCreds.conString, myCreds.userName, myCreds.password, myCreds.dbName)
    update_board = "UPDATE snowboard SET msrp=%s WHERE id=%s " % (priceToUpdate, idToSearch)
    execute_query(conn, update_board)

    return 'Snowboard Updated'


  

app.run()
