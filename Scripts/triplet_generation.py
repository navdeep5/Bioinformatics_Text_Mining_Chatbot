import sqlite3
import json

# Replace 'your_database.db' with the path to your SQLite database file

def generate_relation_jsonl(relation_name, left_table, left_id_column, right_table, right_id_column, middle_string, jsonl_filename):
    # Connect to the SQLite database
    connection = sqlite3.connect('Data/chemfont_sqlite.db')
    cursor = connection.cursor()

    try:
        # Execute a query to retrieve the desired data
        query = f"""
        SELECT {left_table}.name AS left_name, '{middle_string}', {right_table}.name AS right_name
        FROM {relation_name}
        JOIN {left_table} ON {relation_name}.{left_id_column} = {left_table}.{left_id_column}
        JOIN {right_table} ON {relation_name}.{right_id_column} = {right_table}.{right_id_column};
        """
        cursor.execute(query)

        # Fetch all rows from the result set
        data = cursor.fetchall()

        # Save data to a JSON Lines file
        with open(f"Triplets/{jsonl_filename}", 'w') as json_file:
            for row in data:
                triplet = (row[0], middle_string, row[2])
                json_file.write(json.dumps(triplet, separators=(',', ':')) + '\n')

        print(f"Data saved to {jsonl_filename}")

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Example Usage:

# Health Effect Relation
generate_relation_jsonl("health_effect_relation", "compound", "compound_id", "health_effect", "health_effect_id", "causes", "health_effect_relation_triplets.jsonl")

# Process Relation
generate_relation_jsonl("process_relation", "compound", "compound_id", "process", "process_id", "involved in", "process_relation_triplets.jsonl")

# Role Relation
generate_relation_jsonl("role_relation", "compound", "compound_id", "role", "role_id", "has role of", "role_relation_triplets.jsonl")

# Disposition Relation
generate_relation_jsonl("disposition_relation", "compound", "compound_id", "disposition", "disposition_id", "biolocation is", "disposition_relation_triplets.jsonl")

# Exposure Route Relation
generate_relation_jsonl("exposure_route_relation", "compound", "compound_id", "exposure_route", "exposure_route_id", "exposed through", "exposure_route_relation_triplets.jsonl")

# Food Relation
generate_relation_jsonl("food_relation", "compound", "compound_id", "food", "food_id", "sourced through", "food_relation_triplets.jsonl")

# import sqlite3
# import json
# from tqdm import tqdm

# # Replace 'your_database.db' with the path to your SQLite database file

# def generate_relation_jsonl(relation_name, left_table, left_id_column, right_table, right_id_column, middle_string, jsonl_filename):
#     # Connect to the SQLite database
#     connection = sqlite3.connect('Data/chemfont_sqlite.db')
#     cursor = connection.cursor()

#     try:
#         # Execute a query to retrieve the desired data
#         query = f"""
#         SELECT {left_table}.name AS left_name, '{middle_string}', {right_table}.name AS right_name, {relation_name}.external_id
#         FROM {relation_name}
#         JOIN {left_table} ON {relation_name}.{left_id_column} = {left_table}.{left_id_column}
#         JOIN {right_table} ON {relation_name}.{right_id_column} = {right_table}.{right_id_column};
#         """
#         cursor.execute(query)

#         # Fetch all rows from the result set
#         data = cursor.fetchall()

#         # Save data to a JSON Lines file
#         with open(f"Triplets_With_URLs/{jsonl_filename}", 'w') as json_file, tqdm(total=len(data), desc="Processing") as pbar:
#             for row in data:
#                 triplet = (row[0], middle_string, row[2])
#                 external_id = row[3]

#                 if external_id != 'N/A':
#                     # If external_id is not 'N/A', retrieve the URL from cited_external_link
#                     url_query = f"SELECT url FROM cited_external_link WHERE external_id = '{external_id}';"
#                     cursor.execute(url_query)
#                     url_result = cursor.fetchone()
#                     print(f"ID: {external_id}")
#                     if url_result:
#                         url = url_result[0]
#                         json_file.write(json.dumps((triplet, (url,)), separators=(',', ':')) + '\n')
#                 else:
#                     # If external_id is 'N/A', only write the triplet to the file
#                     json_file.write(json.dumps((triplet,), separators=(',', ':')) + '\n')

#                 pbar.update(1)  # Update tqdm progress bar

#         print(f"Data saved to {jsonl_filename}")

#     finally:
#         # Close the cursor and connection
#         cursor.close()
#         connection.close()

# # Example Usage:

# # Health Effect Relation
# generate_relation_jsonl("health_effect_relation", "compound", "compound_id", "health_effect", "health_effect_id", "causes", "health_effect_relation_triplets_with_url.jsonl")

# # Process Relation
# generate_relation_jsonl("process_relation", "compound", "compound_id", "process", "process_id", "involved in", "process_relation_triplets_with_url.jsonl")

# # Role Relation
# generate_relation_jsonl("role_relation", "compound", "compound_id", "role", "role_id", "has role of", "role_relation_triplets_with_url.jsonl")

# # Disposition Relation
# generate_relation_jsonl("disposition_relation", "compound", "compound_id", "disposition", "disposition_id", "biolocation is", "disposition_relation_triplets_with_url.jsonl")

# # Exposure Route Relation
# generate_relation_jsonl("exposure_route_relation", "compound", "compound_id", "exposure_route", "exposure_route_id", "exposed through", "exposure_route_relation_triplets_with_url.jsonl")

# # Food Relation
# generate_relation_jsonl("food_relation", "compound", "compound_id", "food", "food_id", "sourced through", "food_relation_triplets_with_url.jsonl")
