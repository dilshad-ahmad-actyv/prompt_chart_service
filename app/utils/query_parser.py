def extract_sql_query(response_content):
    # Remove code block formatting (```sql and ```)
    response_content = response_content.strip().replace('```sql', '').replace('```', '').strip()
    
    # Normalize whitespace (e.g., multiple spaces, tabs, or newlines to a single space)
    response_content = ' '.join(response_content.split())
    
    # Debugging: Print the cleaned response content
    print('Cleaned response content:', response_content)
    
    # Define the list of SQL keywords to identify the query start
    sql_keywords = ['select', 'insert', 'update', 'delete', 'create', 'drop']
    response_lower = response_content.lower()

    # Find the start of the SQL query
    query_start = next(
        (response_lower.find(keyword) for keyword in sql_keywords if response_lower.find(keyword) != -1), -1
    )
    
    if query_start != -1:
        # Extract the SQL query and clean up extra spaces or newlines
        query = response_content[query_start:].strip()
        # Ensure the query ends with a semicolon
        if not query.endswith(';'):
            query += ';'
        return query
    
    return "No valid query generated."
