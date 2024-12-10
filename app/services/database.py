import pyodbc
from config.settings import DATABASE_CONFIG
import datetime

def get_database_connection():
    conn_str = ";".join(f"{key}={value}" for key,
                        value in DATABASE_CONFIG.items())
    return pyodbc.connect(conn_str)


def get_database_schema():
    conn = get_database_connection()
    cursor = conn.cursor()
    query = """
        SELECT TABLE_NAME, COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        ORDER BY TABLE_NAME, ORDINAL_POSITION;
    """
    cursor.execute(query)
    schema = cursor.fetchall()
    conn.close()

    # Organize schema as a dictionary
    schema_dict = {}
    for table, column in schema:
        if table not in schema_dict:
            schema_dict[table] = []
        schema_dict[table].append(column)
    # print('schema_dict===>\n', schema_dict, '\nschema_dict===>')
    return schema_dict


# def fetch_data(query):
#     conn = get_database_connection()
#     cursor = conn.cursor()
#     cursor.execute(query)
#     rows = cursor.fetchall()
#     conn.close()
#     return rows


# def preprocess_schema(query, cursor):
#     """
#     Dynamically preprocess the schema to cast unsupported types.
#     """
#     # Run the query to fetch metadata
#     sanitized_query = query.strip().rstrip(";")
#     cursor.execute(query)
#     column_descriptions = cursor.description

#     # Build a list of casted columns dynamically
#     casted_columns = []
#     for col_desc in column_descriptions:
#         col_name = col_desc[0]
#         sql_type = col_desc[1]

#         # Check for unsupported data types and apply casting
#         if sql_type == -155:  # DATETIMEOFFSET
#             casted_columns.append(
#                 f"CAST([{col_name}] AS VARCHAR) AS [{col_name}]")
#         elif "timestamp" in col_name.lower() or "datetime" in col_name.lower():
#             casted_columns.append(
#                 f"CAST([{col_name}] AS VARCHAR) AS [{col_name}]")
#         else:
#             casted_columns.append(f"[{col_name}]")

#     # Create a modified query with casting
#     casted_query = f"SELECT {', '.join(casted_columns)} FROM ({sanitized_query}) AS original_query"
#     print('casted_query ->', casted_query)
#     return casted_query

def preprocess_schema(query, cursor):
    """
    Dynamically preprocess the schema to cast unsupported types like bytearray and datetime.datetime.
    """
    # Sanitize the query by removing trailing semicolons
    sanitized_query = query.strip().rstrip(";")

    try:
        # Fetch metadata using a WHERE 1=0 condition to avoid fetching rows
        test_query = sanitized_query + " WHERE 1=0"
        cursor.execute(test_query)
        column_descriptions = cursor.description
    except pyodbc.Error as e:
        print(f"Error during query metadata processing: {e}")
        return sanitized_query  # Return original query if metadata can't be fetched

    # Create a list of columns with necessary casting
    casted_columns = []
    for col_desc in column_descriptions:
        col_name = col_desc[0]
        sql_type = col_desc[1]

        # Apply casting based on the type
        if sql_type == bytearray:  # Handle bytearray columns
            print(f"Column '{col_name}' with type bytearray will be cast to VARCHAR.")
            casted_columns.append(f"CAST([{col_name}] AS VARCHAR) AS [{col_name}]")
        elif sql_type == datetime.datetime:  # Handle datetime columns
            print(f"Column '{col_name}' with type datetime will be cast to VARCHAR.")
            casted_columns.append(f"CAST([{col_name}] AS VARCHAR) AS [{col_name}]")
        else:
            casted_columns.append(f"[{col_name}]")  # No casting needed

    # Replace SELECT * with the list of columns
    modified_query = sanitized_query.replace(
        "SELECT *", f"SELECT {', '.join(casted_columns)}", 1
    )
    print("Modified Query:", modified_query)
    return modified_query

def fetch_data(query):
    print()
    conn = get_database_connection()
    cursor = conn.cursor()

    try:
        # Preprocess the query to handle unsupported column types
        preprocessed_query = preprocess_schema(query, cursor)

        # Execute the modified query
        print("Executing Query:", preprocessed_query)
        cursor.execute(preprocessed_query)
        rows = cursor.fetchall()

        # Fetch column names
        columns = [desc[0] for desc in cursor.description]

        # Convert rows to a list of dictionaries
        results = [dict(zip(columns, row)) for row in rows]

        print('results', results)
        return results

    except pyodbc.Error as e:
        print(f"SQL Error: {e}")
        return []

    finally:
        conn.close()
