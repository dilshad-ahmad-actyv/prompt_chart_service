import pyodbc
from config.settings import DATABASE_CONFIG
import datetime
from dotenv import load_dotenv
import os
import json
load_dotenv()
import decimal

# SERVER = os.getenv('SERVER')
# DATABASE = os.getenv('DATABASE')
# DATABASE_CONFIG = {
#     'DRIVER': '{ODBC Driver 17 for SQL Server}',
#     'SERVER': SERVER,
#     'DATABASE': DATABASE,
#     'Trusted_Connection': 'yes',
#     'TrustServerCertificate': 'yes',
# }

def get_database_connection():
    conn_str = ";".join(f"{key}={value}" for key,
                        value in DATABASE_CONFIG.items())
    return pyodbc.connect(conn_str)

def get_database_schema_relationships():
    conn = get_database_connection()
    cursor = conn.cursor()
    query = """
        SELECT 
    fk.name AS ForeignKeyName,
    tp.name AS ParentTable,
    cp.name AS ParentColumn,
    tr.name AS ReferencedTable,
    cr.name AS ReferencedColumn
FROM 
    sys.foreign_keys AS fk
INNER JOIN 
    sys.foreign_key_columns AS fkc ON fk.object_id = fkc.constraint_object_id
INNER JOIN 
    sys.tables AS tp ON fk.parent_object_id = tp.object_id
INNER JOIN 
    sys.columns AS cp ON fkc.parent_column_id = cp.column_id AND tp.object_id = cp.object_id
INNER JOIN 
    sys.tables AS tr ON fk.referenced_object_id = tr.object_id
INNER JOIN 
    sys.columns AS cr ON fkc.referenced_column_id = cr.column_id AND tr.object_id = cr.object_id
ORDER BY 
    tp.name, fk.name;
    """
    cursor.execute(query)
    schema = cursor.fetchall()
    conn.close()
    # print(schema)

        # Organize the schema into a dictionary
    schema_dict = []
    for row in schema:
        schema_dict.append({
            "ForeignKeyName": row[0],
            "ParentTable": row[1],
            "ParentColumn": row[2],
            "ReferencedTable": row[3],
            "ReferencedColumn": row[4]
        })
        print(schema_dict)
    
    with open('table_relationships.json', 'w') as f:
        json.dump(schema_dict, f, indent=4)
    # Organize schema as a dictionary
    print("Database schema relationships saved to 'database_schema_relationships.json'")

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

        # # Convert rows to a list of dictionaries
        # results = [dict(zip(columns, row)) for row in rows]

        # print('results', results)
        # return results
                # Convert rows to a list of dictionaries
        results = []
        for row in rows:
            row_dict = {}
            for col_name, value in zip(columns, row):
                # If it's a datetime, convert to string (or ISO format)
                if isinstance(value, datetime.datetime):
                    row_dict[col_name] = value.isoformat()
                 # Convert Decimal to float (or str if you prefer)
                elif isinstance(value, decimal.Decimal):
                    row_dict[col_name] = float(value)
                else:
                    row_dict[col_name] = value
            results.append(row_dict)

        return results

    except pyodbc.Error as e:
        print(f"SQL Error: {e}")
        return []

    finally:
        conn.close()
