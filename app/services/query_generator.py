import requests
from config.settings import OPENAI_API_KEY
import pyodbc  # For MS SQL validation
import json
import openai
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

openai.api_key = OPENAI_API_KEY


def load_schema(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading schema: {e}")
        return None


def validate_sql_query(query):
    """
    Validate SQL query against the schema. If not valid, return False.
    Placeholder for actual validation logic (could use `pyodbc` or manual checks).
    """
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=DILSHAD0194;'
            'DATABASE=PD11.2.411;'
            'Trusted_Connection=yes;'
            'TrustServerCertificate=yes;'
        )
        # conn = pyodbc.connect('DRIVER={SQL Server};SERVER=your_server;DATABASE=your_db;UID=user;PWD=password')
        cursor = conn.cursor()
        # Example, adjust depending on your DBMS
        cursor.execute("SET SHOWPLAN_ALL ON;")
        cursor.execute(query)  # This will validate the query without executing it
        cursor.execute("SET SHOWPLAN_ALL OFF;")  # Disable query plan
        return True, ""
        return True, ""
    except pyodbc.Error as e:
        # Capture the error dynamically
        error_message = f"SQL Error: {str(e)}"
        print(f"Validation Error: {error_message}")
        return False, error_message
    finally:
        conn.close()


def generate_sql_query(prompt, schema, entities_actions):
    """
    Generates a SQL query dynamically using OpenAI API based on the prompt and the provided schema.
    Includes retry mechanism for validation.
    """

    # Load schema once
    # file_path = os.path.join(os.path.dirname(
    #     os.path.abspath(__file__)), 'data', 'schema.json')
    # schema = load_schema(file_path)

    # if not schema:
    #     return "Error: Could not load the schema."

    # # Convert schema into a string description for OpenAI (this can be customized based on your needs)
    # schema_description = ''
    # for table in schema:
    #     # Extract table name and columns
    #     table_name = table['table']
    #     columns = table['columns']

    #     # Add basic table and columns information
    #     schema_description += f"Table: {table_name}, Columns: {', '.join(columns)}\n"

    #     # Check if 'data' is present and process the first row for column details
    #     if 'data' in table and table['data']:
    #         # Use the first row of data for example ranges/values
    #         sample_data = table['data'][0]

    #         # Extract column-specific details
    #         for column, value in sample_data.items():
    #             # Handle null or non-informative values
    #             if value is None:
    #                 value_description = "NULL"
    #             elif isinstance(value, bool):
    #                 value_description = f"(e.g.,: {value})"
    #             elif isinstance(value, (int, float)):
    #                 value_description = f"(e.g.,: {value})"
    #             elif isinstance(value, str) and len(value) > 10:  # Trim long strings
    #                 value_description = f"(e.g.,: '{value[:10]}')"
    #             else:
    #                 value_description = f"e.g.,: {value[:10]}"

    #             # Append the description for this column
    #             schema_description += f"    Column '{column}': {value_description}\n"

    # print('schema_description====>', schema_description)
    # Optimized system message
    # system_message = (
    #     "You are a highly skilled SQL assistant. Your task is to generate valid SQL queries for Microsoft SQL Server. "
    #     "You will use the provided schema to identify relevant tables and columns and generate a syntactically correct query."
    #     "Follow these guidelines:\n"
    #     "1. Use the schema to identify tables and columns.\n"
    #     "2. Ensure to match the exact table and column names.\n"
    #     "3. Handle special data formats and conditions, such as ranges and derived metrics.\n"
    #     "4. Use MS SQL Server syntax (e.g., 'TOP' instead of 'LIMIT').\n"
    #     "5. If the request cannot be fulfilled, respond with 'The schema does not support this request.'\n"
    #     "6. Addressing any issues or errors in previously generated queries, including syntax errors, invalid column or table names, "
    #     "or logical inconsistencies.\n"

    #     "7. End the query with a semicolon.\n\n"
    #     "8. If the query fails, identify and fix errors based on provided error messages.\n"
    #     f"Here is the provided schema:\n{schema_description}\n"
    # )

    system_message = (
        "You are a highly skilled SQL assistant. Generate valid SQL queries for Microsoft SQL Server based on the provided schema context. "
        "Follow these guidelines:\n"
        "- Use exact table and column names.\n"
            "- Use aggregation functions (COUNT, SUM, AVG, etc.) with meaningful aliases (e.g., 'AS TotalSum', 'AS AverageValue').\n"
        "- Use SQL Server syntax (e.g., 'TOP' instead of 'LIMIT').\n"
        "- End every query with a semicolon.\n"
    )

    # Optimized user message
    user_message = (
    f"User Prompt: {prompt}\n"
    "Generate a SQL query based on the provided schema. The schema includes table names, column names, and sample data.\n"
    "- Use the exact table and column names from the schema.\n"
    "- Refer to the sample data for additional context, such as value ranges.\n"
    "- Include conditions like WHERE, HAVING, JOIN if required by the prompt.\n"
    "- Use aggregation functions (COUNT, SUM, AVG, etc.) with meaningful aliases (e.g., 'AS TotalSum', 'AS AverageValue').\n"
    "- Ensure the query is syntactically correct for MS SQL Server.\n"
    "- Write the query in a single line without newline ('\\n') characters.\n"
    "- Remove any unnecessary whitespace and ensure proper formatting.\n"
    "- End the query with a semicolon.\n"
    "- Schema Context:\n"
    f"{entities_actions}\n"
    "- If no valid query can be generated, respond with 'The schema does not support this request.'"
)


    # user_message = (
    #     f"User Prompt: {prompt}\n"
    #     "Generate a valid SQL query that aligns with the user's request and schema."
    # )

    # OpenAI API call to generate SQL query
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": system_message},
                  {"role": "user", "content": user_message}],
    )

    query = response['choices'][0]['message']['content'].strip()
    query = query.replace("```sql", "").replace("```", "").strip()
    print('============query=============>', query)
    return query
    # Validate query before returning
    # retry_count = 0
    # error_message = ""
    # while retry_count < 3:
    #     is_valid, error_message = validate_sql_query(query)
    #     print('isvalid------------>', is_valid)
    #     print('error_message------------>', error_message)

    #     if is_valid:
    #         return query
    #     retry_count += 1

    #     # Retry by regenerating the query
    #     response = openai.ChatCompletion.create(
    #         model="gpt-4",
    #         messages=[
    #             {"role": "system", "content": system_message},
    #             {
    #                 "role": "user",
    #                 "content": (
    #                     f"User Prompt: {prompt}\n\n"
    #                     f"Previous Error: {error_message}\n"
    #                     "Regenerate the query to address the above error."
    #                 ),
    #             },],
    #     )

    #     query = response['choices'][0]['message']['content'].strip()
    #     query = query.replace("```sql", "").replace("```", "").strip()
    #     print('retry_count: ', retry_count)
    # return query if validate_sql_query(query) else "Error: Generated query is invalid after 3 retries."
