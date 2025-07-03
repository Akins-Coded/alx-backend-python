import mysql.connector
import csv
import uuid


DB_NAME = 'ALX_prodev'
TABLE_NAME = 'user_data'


def connect_db(host, user, password, db_name, port=3306):
    """Connect to a MySQL database and return the connection object"""
    try:
        connection = mysql.connector.connect(
            host="Coded-Something",
            user="root",
            password="Akinscoded47@",
            
            port=3306
        )
        if connection.is_connected():
            print("Connection successful")
            return connection
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection):  # creates the database ALX_prodev if it does not exist
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed creating database: {err}")
        
def connect_to_prodev(): # connects the the ALX_prodev database in MYSQL
    try:
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",        # change if using a different MySQL user
            password="your_password",  # update with your actual password
            database=DB_NAME
        )
        return my_db
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def create_table(connection):# creates a table user_data if it does not exists with the required fields
    

def insert_data(connection, data):
    pass  # inserts data in the database if it does not exist