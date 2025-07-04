import mysql.connector
import csv
import uuid
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_NAME = 'ALX_prodev'
TABLE_NAME = 'users'

def connect_db():
    """Connect to MySQL server (without selecting a specific DB)."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        if connection.is_connected():
            print("✅ Connection successful")
            return connection
    except mysql.connector.Error as e:
        print(f"❌ Error: {e}")
    return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        connection.commit()
        cursor.close()
        print("✅ Database checked/created.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating database: {err}")

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            print("✅ Connected to ALX_prodev")
            return connection
    except mysql.connector.Error as err:
        print(f"❌ Error: {err}")
    return None

def create_table(connection):
    """Create the users table if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                age INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        cursor.close()
        print("✅ Table 'users' created successfully.")
    except Exception as e:
        print(f"❌ Error creating table: {e}")

def insert_data(connection, csv_filename):
    """Insert data into the users table from a CSV file."""
    try:
        cursor = connection.cursor()
        with open(csv_filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                cursor.execute(f"SELECT email FROM {TABLE_NAME} WHERE email = %s", (row['email'],))
                if cursor.fetchone():
                    continue
                user_id = str(uuid.uuid4())
                cursor.execute(f"""
                    INSERT INTO {TABLE_NAME} (id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, row['name'], row['email'], row['age']))
        connection.commit()
        cursor.close()
        print("✅ Data inserted successfully.")
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
