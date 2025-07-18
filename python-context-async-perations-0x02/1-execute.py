import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(f"[ERROR] Query failed: {exc_val}")
        if self.conn:
            self.conn.commit()
            self.conn.close()
# ✅ Use the context manager to execute a query and print results
with ExecuteQuery("users.db", "SELECT * FROM users") as results:
    print("[RESULTS]", results) # ✅ Use the context manager to execute a query with parameters
with ExecuteQuery("users.db", "SELECT * FROM users WHERE age > ?", (25,)) as results:
    print("[RESULTS]", results)  # ✅ Use the context manager to execute an insert query    