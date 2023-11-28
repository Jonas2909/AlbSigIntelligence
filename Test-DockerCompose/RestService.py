from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import bcrypt
from database import (
    get_all_users,
    get_user_by_username,
    add_user_to_database,
    delete_user_by_username,
    check_if_user_exists_by_username,
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

    if username:
        result = get_user_by_username(username)
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

    salt = bcrypt.gensalt(rounds=10)
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    if username and password:
        existing_user_response = check_if_user_exists_by_username(username)
        if existing_user_response:
            abort(404, "Username already exists. Please choose a different username.")
        else:
            result = add_user_to_database(firstname, lastname, username, hashed_password)
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)