import mysql.connector

def stream_users():
    """Generaor that yields users from a MySQL database."""
    
    try:
        connection =mysql.connector.connect(
            host='localhost',
            user='root',
            password='#########',  # Update with your actual password
            database='ALX_prodev',
            port=3306  # Default MySQL port
        )
        cursor = connection.cursor(dictionary=True)

        cursor.excecute("SELECT id, first_name, last_name, email, age FROM users")
        for row in cursor:
            yield row
            
            cursor.close()
            connection.close()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return
    