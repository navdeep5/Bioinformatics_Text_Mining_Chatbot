# sql_file_path = 'Data/chemfont030923.sql' # Replace with the actual path to your SQL file

# with open(sql_file_path, 'r') as sql_file:
#     for line in sql_file:
#         print(line.strip())  # Remove leading/trailing whitespaces


import psycopg2
import pandas as pd
from io import StringIO
import re

# Replace these with your PostgreSQL connection details
db_params = {
    'host': 'localhost',
    'port': '5432',
    'database': 'ChemFont',
    'user': 'root',
    'password': '123'
}

# Replace with the actual path to your PostgreSQL dump file
sql_file_path = 'Data/chemfont030923.sql'

'''
# Define a regular expression to match CREATE TABLE statements and extract table names
create_table_pattern = re.compile(r'CREATE TABLE ([^\s\(]+)')

# List to store table names
table_names = []

# Initialize the cursor and connection outside the try block
cursor = None
connection = None

try:
    # Open the file in binary mode and manually handle decoding
    with open(sql_file_path, 'rb') as sql_file:
        sql_script_bytes = sql_file.read()
        sql_script = sql_script_bytes.decode('utf-8', errors='replace')

        # Find all matches of CREATE TABLE statements
        matches = create_table_pattern.findall(sql_script)

        # Extract and print table names
        for match in matches:
            table_names.append(match)

    print("Tables in the PostgreSQL dump file:")
    for table_name in table_names:
        print(table_name)

    # Connect to a PostgreSQL database and retrieve the list of tables
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    # Fetch the list of tables
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    postgresql_tables = cursor.fetchall()

    print("\nTables in the PostgreSQL database:")
    for table in postgresql_tables:
        print(table[0])

finally:
    # Close the connection and cursor if they were successfully opened
    if cursor:
        cursor.close()
    if connection:
        connection.close()
'''


# Specify the table you want to view
table_name = 'biomarker'

cursor = None
connection = None

try:
    # Open the SQL file and execute its contents
    with open(sql_file_path, 'rb') as sql_file:
        sql_script_bytes = sql_file.read()
        sql_script = sql_script_bytes.decode('utf-8', errors='replace')

        # Connect to the PostgreSQL database
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Execute the SQL script
        cursor.execute(sql_script)

        # Execute a SELECT query on the specified table
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Display the results
        print(f"Contents of the '{table_name}' table:")
        for row in rows:
            print(row)

finally:
    # Close the connection and cursor
    if cursor:
        cursor.close()
    if connection:
        connection.close()