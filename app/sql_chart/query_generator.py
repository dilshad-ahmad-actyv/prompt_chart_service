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
        "1. ##Analyze the user prompt, its context data, and table relationships.##"
        "2. Identify which tables and columns are needed based on the user's question."
        "3. For the `EpiUsers` table, always join with its `Id` column and the `UserId` column of any related table when relationships exist. "
        "4. In the response, concatenate `FirstName` and `LastName` as `name` using `CONCAT` or equivalent SQL syntax, and ensure the `name` column is included in the final output. "
        "6. When ordering results, use only columns explicitly mentioned in the metadata, relationships, or user query. Do not assume the existence of columns like `PerformanceMetric` unless they are explicitly defined. "
        "7. Use subqueries or aggregate functions (e.g., COUNT, SUM) only if explicitly required or implied by the user's query. "
        "8. Always generate queries compatible with MSSQL syntax: "
        "   - Use `TOP` instead of `LIMIT` for limiting results."
        "   - Avoid non-MSSQL-specific syntax such as backticks for column/table names."
        "   - Ensure `ORDER BY` clauses use valid columns and are logically aligned with the query intent. "
        "9. Use table relationships (e.g., JOINs) only if the user's query requires it or if relationships are implied by the data."
        "10. Use `SUBSTRING` or similar functions only when applicable, and ensure accurate filtering in the query."
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
### Task:
0. ##Analyze the user prompt, its intensions, its context data, and table relationships.##"
1. Identify which tables and columns are needed based on the user's question.
2. If the user’s question implies data from multiple tables, then join those tables using the relationships provided.
3. For the EpiUsers table(if it requires based on the User Query), remember:
   - Use EpiUsers.Id for joins with related tables' UserId column.
   - Concatenate FirstName and LastName as name, include in the SELECT.
4. Use valid MSSQL syntax (no backticks, use TOP instead of LIMIT, etc.).
5. **Only** output the final SQL query—no extra commentary.
6. Ensure `ORDER BY` clauses use only valid columns explicitly mentioned in the metadata, relationships, or user query.
7. Generate a valid MSSQL query that satisfies the user's intent, ensuring proper MSSQL syntax as described above.
8. ##Give only the result as per the user query, ensuring the query fully meets the user’s requirements##.
9. **Handling AHT as a range**:\n"
        "   - If the user asks for an 'average' of AHT or implies numeric operations on the AHT column, note that AHT is stored as a string in the format 'xx-yy'.\n"
        "   - To compute a row-level average of AHT, split on '-', cast each side to `INT`, and compute `(min_val + max_val)/2`.\n"
        "   - If the user wants the average across all rows (an overall average), wrap the row-level expression with an `AVG(...)`. For instance:\n"
        "     AVG(\n"
        "       (\n"
        "         CAST(LEFT(AHT, CHARINDEX('-', AHT) - 1) AS INT)\n"
        "         + CAST(RIGHT(AHT, LEN(AHT) - CHARINDEX('-', AHT)) AS INT)\n"
        "       ) / 2.0\n"
        "     )\n"
        "   - Only do this parsing and averaging if the user’s query explicitly or implicitly requires numeric operations on AHT. Otherwise, treat it as a plain string.\n"
        "\n"
**Response Format:**
The output must only contain the SQL query, without any additional explanations or comments.
"""
    
    response = generate_response(system_prompt, user_prompt, model)
    return response

# def process_query_and_generate_sql_query(headers, user_query, relations, model):
#     system_prompt = (
#         "You are an expert in generating MSSQL queries. Your task is to analyze the user prompt, provided Context Data, "
#         "and the table relationships. Generate an accurate SQL query that aligns with MSSQL syntax. "
#         "The response must be **an exact SQL query only**, without any explanations or additional comments. "
#         "Ensure the query incorporates relevant column values from the context and uses JOINs or filters only if required "
#         "based on the user's query or implied by the relationships between tables. "
#         "Key requirements: "
#         "1. For the `EpiUsers` table, use the `Id` column for joins or filters when referring to user-specific data. "
#         "2. Always check if the user input (e.g., 'Amit') matches `FirstName` or `LastName`. Use `OR` conditions to handle such scenarios dynamically. "
#         "3. Avoid assumptions about columns unless explicitly mentioned in the metadata or relationships. "
#         "4. Use `SUBSTRING` or similar functions only when applicable, and ensure accurate filtering in the query."
#     )
        
#     user_prompt = f"""I have a list of database tables with detailed metadata about their columns(headers), sample data, and relationships. 
# Based on the following user query, analyze the context and generate a precise SQL query.

# ### Context Data:
# {json.dumps(headers, indent=2)}

# ### Table Relationships:
# {json.dumps(relations, indent=2)}

# ### User Query:
# "{user_query}"

# ### Task:
# 1. Identify the relevant tables, columns, and relationships based on the user's query.
# 2. For the `EpiUsers` table, ensure the `Id` column is used for joins or filters. Use `FirstName` and `LastName` in `OR` conditions when filtering by name.
# 3. Consider column values provided in the context to add accurate filtering conditions (e.g., WHERE clauses).
# 4. Use table relationships (e.g., JOINs) only if the user's query requires it or if relationships are implied by the data.
# 5. Generate a valid SQL query specifically for MSSQL that satisfies the user's intent.

# **Response Format:**
# The output must only contain the SQL query, without any additional explanations or comments.
# """
    
#     response = generate_response(system_prompt, user_prompt, model)
#     return response


