import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql_chart.model_config import generate_response
def process_query_and_generate_sql_query(headers, user_query):

    system_prompt = "You are an expert in generating MSSQL queries. Your task is to analyze the user prompt and provided table metadata, including column values, to generate an accurate SQL query. The response must be **an exact SQL query only**, without any explanations or additional comments. Ensure the query aligns with MSSQL syntax, incorporates relevant column values, and uses JOINs or filters only if required by the query or implied by the column relationships."

    user_prompt = f"""I have a list of database tables with detailed metadata about their columns and sample data. Based on the following user query, analyze the context and generate a precise SQL query.

### Context Data:
{json.dumps(headers, indent=2)}

### User Query:
"{user_query}"

### Task:
1. Identify the relevant tables and columns based on the user's query.
2. Consider column values provided in the context to add accurate filtering conditions (e.g., WHERE clauses).
3. Use table relationships (e.g., JOINs) only if the user's query requires it or if implied by column relationships.
4. Generate a valid SQL query specifically for MSSQL that satisfies the user's intent.

**Response Format:** The output must only contain the SQL query, without any additional explanations or comments.

For example:
```sql
SELECT [Column1], [Column2]
FROM [Table1]
WHERE [Column3] = 'value';"""
    
    response = generate_response(system_prompt, user_prompt)
    return response