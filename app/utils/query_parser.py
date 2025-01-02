def extract_sql_query(response_content):
    response_content = response_content.replace('\n', ' ')
    print('response_content: ', response_content)
    sql_keywords = ['select', 'insert', 'update', 'delete', 'create', 'drop']
    response_lower = response_content.lower()

    query_start = next(
        (response_lower.find(keyword) for keyword in sql_keywords if response_lower.find(keyword) != -1), -1
    )
    if query_start != -1:
        query = response_content[query_start:].split(';')[0].strip() + ';'
        return query
    return "No valid query generated."
