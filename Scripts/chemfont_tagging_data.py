import sqlite3
from tqdm import tqdm

# Connect to the SQLite database
conn = sqlite3.connect('Data/chemfont_sqlite.db')
cursor = conn.cursor()

# Define a function to execute a query and retrieve names from a table
def get_names(table_name):
    query = f"SELECT name FROM {table_name}"
    cursor.execute(query)
    return set(row[0] for row in cursor.fetchall())

# Define the table names
# table_names = ['compound', 'compound_source', 'disposition', 'exposure_route', 
            #    'food_relation', 'health_effect', 'organoleptic_effect', 'process', 'role']
table_names = ['biomarker']

# Iterate over table names and retrieve names for each table
for table_name in table_names:
    names = get_names(table_name)
    # Save names to a text file
    with open(f"ChemFont_Tagging/{table_name}_names.txt", 'w', encoding='utf-8') as f:
        for name in tqdm(names, desc=f"Saving {table_name}"):
            f.write(f"{name}\n")

# Close the database connection
conn.close()
