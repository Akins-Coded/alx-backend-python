
# 📦 Seed Script for `ALX_prodev` MySQL Database

This project contains a Python script `seed.py` that connects to a MySQL server, creates a database and a table, and populates it with user data from a CSV file.

## 🗂️ Project Structure

```
.
├── seed.py
├── user_data.csv
└── 0-main.py
```

## ✅ Features

- Connects to a MySQL server
- Creates a database named `ALX_prodev` if it doesn't exist
- Creates a table `user_data` with the following fields:
  - `id` (UUID, Primary Key)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL, UNIQUE)
  - `age` (INT, NOT NULL)
  - `created_at` (Timestamp, defaults to current time)
- Loads and inserts records from a CSV file (e.g., `user_data.csv`)
- Skips inserting records if the email already exists in the database

## 🛠️ Requirements

- Python 3.6+
- MySQL Server
- Required Python Packages:
  ```bash
  pip install mysql-connector-python
  ```

## 📥 Setup

1. **Clone the repository (or copy the files into a project directory).**

2. **Update MySQL credentials**  
   In `seed.py`, modify the following values in `connect_db()` and `connect_to_prodev()`:
   ```python
   host="localhost"
   user="root"
   password="your_password"
   ```

3. **Prepare your CSV file:**  
   Ensure the file `user_data.csv` exists in the same directory and has this format:

   ```csv
   name,email,age
   John Doe,johndoe@example.com,35
   Jane Smith,janesmith@example.com,28
   ```

## 🚀 Usage

Run the seeding process through `0-main.py`:

```bash
chmod +x 0-main.py
./0-main.py
```

You should see output like:

```
Connection successful
Table 'user_data' created successfully.
Database ALX_prodev is present 
[('uuid1', 'John Doe', 'johndoe@example.com', 35), ...]
```

## 🔧 Main Functions Overview

- **`connect_db(host, user, password, db_name, port)`**  
  Connects to MySQL server (without selecting a database).

- **`create_database(connection)`**  
  Creates the `ALX_prodev` database if it doesn't exist.

- **`connect_to_prodev()`**  
  Connects to the `ALX_prodev` database.

- **`create_table(connection)`**  
  Creates the `user_data` table with all required columns.

- **`insert_data(connection, csv_filename)`**  
  Loads users from `user_data.csv` and inserts them into the database.

## ⚠️ Notes

- Avoid using `" "` (a space) as the password — use an empty string `""` or your actual password.
- Ensure MySQL is running before executing the script.
- The `email` field is unique — duplicate emails will be skipped.

## 👩🏽‍💻 Author

Muheez Akindipe  
