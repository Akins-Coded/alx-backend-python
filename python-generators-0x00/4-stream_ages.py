import mysql.connector
from dotenv import load_dotenv
import os

def stream_user_ages():
    """Generator that streams user ages from the database."""

    # Load environment variables
    load_dotenv()

    # Connect to the database
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM users")

    for row in cursor:  # Loop 1
        yield row['age']

    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculate and print the average age using a generator."""
    total_age = 0
    count = 0

    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1

    if count > 0:
        avg = total_age / count
        print(f"Average age of users: {avg:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    calculate_average_age()
