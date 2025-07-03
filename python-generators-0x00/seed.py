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
def create_table(connection):
    """Creates a table 'user_data' if it does not exist with the required fields"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        cursor.close()
        print("Table 'user_data' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")


def insert_data(connection, user_data): # inserts data in the database if it does not exist
     """Insert data into user_data table from CSV file"""
try:
        cursor = connection.cursor()
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if email already exists to avoid duplicates
                cursor.execute(f"SELECT email FROM {TABLE_NAME} WHERE email = %s", (row['email'],))
                if cursor.fetchone():
                    continue

                uid = str(uuid.uuid4())
                cursor.execute(f"""
                    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (uid, row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
except Exception as e:
        print(f"Error inserting data: {e}")
