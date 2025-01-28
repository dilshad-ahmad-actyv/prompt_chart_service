import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql_chart.model_config import generate_response

def process_query_and_generate_sql_query(headers, user_query, relations, model):
    system_prompt = (
        "You are an expert in generating MSSQL queries. Your task is to analyze the user prompt, provided Context Data, "
        "and the table relationships. Generate an accurate SQL query that aligns with MSSQL syntax. "
        "The response must be **an exact SQL query only**, without any explanations or additional comments. "
        "Ensure the query incorporates relevant column values from the context and uses JOINs or filters only if required "
        "based on the user's query or implied by the relationships between tables. "
        "Key requirements: "
        "1. For the `EpiUsers` table, use the `Id` column for joins or filters when referring to user-specific data. "
        "2. Always check if the user input (e.g., 'Amit') matches `FirstName` or `LastName`. Use `OR` conditions to handle such scenarios dynamically. "
        "3. Avoid assumptions about columns unless explicitly mentioned in the metadata or relationships. "
        "4. Use `SUBSTRING` or similar functions only when applicable, and ensure accurate filtering in the query."
    )
        
    user_prompt = f"""I have a list of database tables with detailed metadata about their columns(headers), sample data, and relationships. 
Based on the following user query, analyze the context and generate a precise SQL query.

### Context Data:
{json.dumps(headers, indent=2)}

### Table Relationships:
{json.dumps(relations, indent=2)}

### User Query:
"{user_query}"

### Task:
1. Identify the relevant tables, columns, and relationships based on the user's query.
2. For the `EpiUsers` table, ensure the `Id` column is used for joins or filters. Use `FirstName` and `LastName` in `OR` conditions when filtering by name.
3. Consider column values provided in the context to add accurate filtering conditions (e.g., WHERE clauses).
4. Use table relationships (e.g., JOINs) only if the user's query requires it or if relationships are implied by the data.
5. Generate a valid SQL query specifically for MSSQL that satisfies the user's intent.

**Response Format:**
The output must only contain the SQL query, without any additional explanations or comments.
"""
    
    response = generate_response(system_prompt, user_prompt, model)
    return response