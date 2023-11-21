from flask import Flask, jsonify, request, abort
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

database_name = "exampledb"
user = "postgres"
password = "mysecretpassword"
host = "local_db"
port = "5432"

def connect_to_database():
    try:
        conn = psycopg2.connect(
            database=database_name,
            user=user,
            password=password,
            host=host,
            port=port
        )

        return conn
    except psycopg2.Error as e:
        print("Error connecting to the PostgreSQL database:", e)
        return None

def get_user_by_username(username):
    conn = connect_to_database()
    if conn is None:
        abort(500, "Error connecting to the PostgreSQL database.")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_credentials WHERE username = %s", (username,))
        row = cursor.fetchone()

        if row:
            user_dict = {
                'id': row[0],
                'firstname': row[1],
                'lastname': row[2],
                'username': row[3],
                'password': row[4]
            }
            cursor.close()
            conn.close()
            return jsonify(user=user_dict)
        else:
            cursor.close()
            conn.close()
            abort(404, "User not found.")

    except psycopg2.Error as e:
        abort(500, "Error executing SQL query: " + str(e))

def check_if_user_exists_by_username(username):
    conn = connect_to_database()
    if conn is None:
        abort(500, "Error connecting to the PostgreSQL database.")

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_credentials WHERE username = %s", (username,))
        row = cursor.fetchone()

        if row:
            user_dict = {
                'id': row[0],
                'firstname': row[1],
                'lastname': row[2],
                'username': row[3],
                'password': row[4]
            }
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False

    except psycopg2.Error as e:
        abort(500, "Error executing SQL query: " + str(e))
        
def add_user_to_database(firstname, lastname, username, password):
    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_credentials (firstname, lastname, username, password) VALUES (%s, %s, %s, %s)", (firstname, lastname,  username, password))
        conn.commit()
        cursor.close()
        conn.close()
        return "User added to the database."

    except psycopg2.Error as e:
        return "Error adding user to the database: " + str(e)

def delete_user_by_username(username):
    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_credentials WHERE username = %s", (username,))
        conn.commit()
        cursor.close()
        conn.close()
        return "User deleted from the database."

    except psycopg2.Error as e:
        return "Error deleting user from the database: " + str(e)

@app.route("/Hello")
def hello_world():
    return "Hello, World!"

@app.route("/GetAllUsers")
def get_all_users():
    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_credentials")
        rows = cursor.fetchall()
        user_list = []
        for row in rows:
            user_dict = {
                'id': row[0],
                'firstname': row[1],
                'lastname': row[2],
                'username': row[3],
                'password': row[4]
            }
            user_list.append(user_dict)
        cursor.close()
        conn.close()
        return jsonify(users=user_list)

    except psycopg2.Error as e:
        return "Error executing SQL query: " + str(e)

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)