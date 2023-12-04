import psycopg2
import bcrypt
from flask import abort, jsonify
import logging

database_name = "exampledb"
user = "postgres"
password = "mysecretpassword"
host = "local_db"
port = "5432"

logging.basicConfig(level=logging.DEBUG)

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

def get_user_by_username_and_password(username, password):
    conn = connect_to_database()
    if conn is None:
        return {'error': 'Error connecting to the PostgreSQL database.'}, 500

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

            hashed_password_from_db = user_dict['password'].encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password_from_db):
                cursor.close()
                conn.close()
                return {'message': 'Correct password.'}

            else:
                cursor.close()
                conn.close()
                return {'error': 'Incorrect password.'}, 401

        else:
            cursor.close()
            conn.close()
            return {'error': 'User not found.'}, 404

    except psycopg2.Error as e:
        return {'error': 'Error executing SQL query: ' + str(e)}, 500

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

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    hased_password_decoded = hashed_password.decode('utf-8')
    
    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_credentials (firstname, lastname, username, password) VALUES (%s, %s, %s, %s)", (firstname, lastname,  username, hased_password_decoded))
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
        
### start insert test data
def add_graph_data_database(time_stamp, quantity):
    conn = connect_to_database()

    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO measurements (time_stamp, quantity) VALUES (%s, %s)", (time_stamp, quantity))
        conn.commit()
        cursor.close()
        conn.close()
        return "Data added to the database."

    except psycopg2.Error as e:
        return "Error adding Data to the database: " + str(e)
### end insert test data

### start read test data
def get_graph_data():
    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM measurements")
        rows = cursor.fetchall()
        data_list = []
        for row in rows:
            data_dict = {
                'id': row[0],
                'time_stamp': row[1],
                'quantity': row[2]
            }
            data_list.append(data_dict)
        cursor.close()
        conn.close()
        return jsonify(data=data_list)

    except psycopg2.Error as e:
        return "Error executing SQL query: " + str(e)
### end read test data
