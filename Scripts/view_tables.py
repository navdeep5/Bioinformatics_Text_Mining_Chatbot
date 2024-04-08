import sqlite3

# Replace 'your_database.db' with the path to your SQLite database file
database_path = 'Data/chemfont_sqlite.db'
# Replace 'your_table_name' with the name of the specific table you want to view
table_name = 'biomarker'
# Connect to the SQLite database
connection = sqlite3.connect(database_path)
# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Execute a PRAGMA query to get column information for the specific table
cursor.execute(f"PRAGMA table_info({table_name});")
columns_info = cursor.fetchall()

# Extract and print the column names
column_names = [column[1] for column in columns_info]
print(f"Column names of the '{table_name}' table: {column_names}")

# Execute a SELECT query on the specific table
cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
table_content = cursor.fetchall()

# Display the content of the table
print(f"\nContents of the '{table_name}' table:")
for row in table_content:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()
