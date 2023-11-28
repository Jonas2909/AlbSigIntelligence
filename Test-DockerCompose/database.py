import psycopg2
from flask import abort, jsonify

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
