import mysql.connector

def stream_users_in_batches(batch_size):
    """Generator that yields users in batches of size `batch_size`."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="##########",  # Replace with MySQL Database password
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT id, first_name, last_name, email, age FROM user_data")

        batch = []
        for row in cursor:  # Loop 1
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        if batch:  # yield last remaining batch
            yield batch

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return


def batch_processing(batch_size):
    """Processes batches and prints users with age > 25"""
    for batch in stream_users_in_batches(batch_size):  # Loop 2
        for user in batch:  # Loop 3
            if int(user['age']) > 25:
                print(user)
