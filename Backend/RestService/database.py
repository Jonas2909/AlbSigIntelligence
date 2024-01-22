import psycopg2
import bcrypt
from flask import abort, jsonify
import logging
import hashlib


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
        
def add_graph_data_database(time_stamp, value, is_quantity=True):
    conn = connect_to_database()

    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        if is_quantity:
            # Treat the value as quantity
            cursor.execute("INSERT INTO measurements (time_stamp, quantity) VALUES (%s, %s)", (time_stamp, value))
        else:
            # Treat the value as mac_address
            cursor.execute("INSERT INTO mac_addresses (time_stamp, hashed_mac_address) VALUES (%s, %s)", (time_stamp, value))
        conn.commit()
        cursor.close()
        conn.close()
        return "Data added to the database."

    except psycopg2.Error as e:
        return "Error adding Data to the database: " + str(e)
        
        
def delete_hash_database(time_stamp):
    if time_stamp != "doit":
        return "Wong Key!"

    time_stamp = 1702915589
    value = 'e140ef2f06fc2fac86f1e446149b890f6b762da78b7b3109df6cc49c9b29dec1'
    time_stamp_2 = 1703174789
    value_2 = 'a56b61402f0913c69785a9df529f78658dcae766f619f3129b07bb6c5861578d'

    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM mac_addresses")
        conn.commit()
        cursor.execute("INSERT INTO mac_addresses (time_stamp, hashed_mac_address) VALUES (%s, %s)", (time_stamp, value))
        conn.commit()
        cursor.execute("INSERT INTO mac_addresses (time_stamp, hashed_mac_address) VALUES (%s, %s)", (time_stamp_2, value_2))
        conn.commit()
        cursor.close()
        conn.close()
        return "Deleted old MAC-Addresses"

    except psycopg2.Error as e:
        return "Error executing SQL query: " + str(e)

        
        

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


def get_hashed_mac_addresses():
    conn = connect_to_database()

    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM mac_addresses")
        rows = cursor.fetchall()
        data_list = []

        for row in rows:
            data_dict = {
                'id': row[0],
                'time_stamp': row[1],
                'hashed_mac_address': row[2]
            }
            data_list.append(data_dict)

        cursor.close()
        conn.close()
        return jsonify(data=data_list)

    except psycopg2.Error as e:
        return "Error executing SQL query: " + str(e)


def get_graph_data_from_to(timestamp_from, timestamp_to):
    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM measurements WHERE time_stamp BETWEEN %s AND %s"
        cursor.execute(query, (timestamp_from, timestamp_to))
        rows = cursor.fetchall()

        logging.info(rows)

        data_list = []
        for row in rows:
            data_dict = {
                'id': row[0],
                'time_stamp': row[1],
                'quantity': row[2],
            }
            data_list.append(data_dict)

        cursor.close()
        conn.close()
        return jsonify(data=data_list)

    except psycopg2.Error as e:
        return "Error executing SQL query: " + str(e)

def get_entries_by_mac_address(mac_address):
    conn = connect_to_database()
    if conn is None:
        return "Error connecting to the PostgreSQL database."

    hashed_mac_address = hashlib.sha256(mac_address.encode()).hexdigest()
    logging.info(hashed_mac_address)

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM mac_addresses WHERE hashed_mac_address = %s"
        cursor.execute(query, (hashed_mac_address,))
        rows = cursor.fetchall()

        entries_list = []
        for row in rows:
            entry_dict = {
                'id': row[0],
                'time_stamps': row[1],
                'mac_address': row[2],
            }
            entries_list.append(entry_dict)

        cursor.close()
        conn.close()
        return jsonify(entries=entries_list)

    except psycopg2.Error as e:
        return "Error executing SQL query: " + str(e)
