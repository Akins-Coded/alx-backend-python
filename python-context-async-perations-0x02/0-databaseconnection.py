import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor  # returned object used in the `with` block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_val}")
        if self.conn:
            self.conn.commit()
            self.conn.close()

# ✅ Use the context manager to fetch and print all users
with DatabaseConnection("users.db") as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("[RESULTS]", results)
