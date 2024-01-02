from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from database import (
    get_all_users,
    get_user_by_username_and_password,
    add_user_to_database,
    delete_user_by_username,
    check_if_user_exists_by_username,
    add_graph_data_database,
    get_graph_data,
    get_graph_data_from_to,
    get_entries_by_mac_address,
)

app = Flask(__name__)
CORS(app)

@app.route("/Hello")
def hello_world():
    return "Hello, World!"

@app.route("/GetAllUsers")
def get_all_users_route():
    return get_all_users()

@app.route("/GetUser", methods=['POST'])
def get_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username:
        result = get_user_by_username_and_password(username, password)
        return result
    else:
        return "Invalid data. 'username' is required in the request."

@app.route("/AddUser", methods=['POST'])
def add_user():
    data = request.get_json()
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        existing_user_response = check_if_user_exists_by_username(username)
        if existing_user_response:
            abort(404, "Username already exists. Please choose a different username.")
        else:
            result = add_user_to_database(firstname, lastname, username, password)
            return result
    else:
        return "Invalid data. 'firstname', 'lastname', 'username', and 'password' are required in the request."

@app.route("/DeleteUser", methods=['DELETE'])
def delete_user():
    data = request.get_json()
    username = data.get('username')

    if username:
        result = delete_user_by_username(username)
        return result
    else:
        return "Invalid data. 'username' is required in the request."

@app.route("/AddGraphData", methods=['POST'])
def add_graph_data():
    data = request.get_json()
    time_stamp = data.get('time_stamp')
    quantity = data.get('quantity')
    hashed_mac_address = data.get('hashed_mac_address')

    if time_stamp and (quantity or hashed_mac_address):
        if quantity:
            result = add_graph_data_database(time_stamp, quantity)
        elif hashed_mac_address:
            result = add_graph_data_database(time_stamp, hashed_mac_address, is_quantity=False)
        return result
    else:
        abort(404, "Error Adding Graph Data to database.")

@app.route("/GetGraphData", methods=['GET'])
def get_graph_data_route():
    return get_graph_data()

@app.route("/GetGraphDataFromTo", methods=['POST'])
def get_graph_data_from_to_route():
    data = request.get_json()
    time_stamp_from = data.get('time_stamp_from')
    time_stamp_to = data.get('time_stamp_to')
    if time_stamp_from and time_stamp_to:
        result = get_graph_data_from_to(time_stamp_from, time_stamp_to)
        return result
    else:
        abort(404, "Invalid data. Timestamps are required in the request")

@app.route("/GetTimeStampsByMac", methods=['POST'])
def get_timestamps_by_mac_route():
    data = request.get_json()
    mac = data.get('mac_address')
    if mac:
        result = get_entries_by_mac_address(mac)
        return result
    else:
        abort(404, "Invalid data. MAC-Address is required in the request")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
