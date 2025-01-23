import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# from fastapi import FastAPI, HTTPException
import json
from sql_chart.model_config import generate_response
from sql_chart.fetch_records_from_header import fetch_records_from_header_table
from sql_chart.query_generator import process_query_and_generate_sql_query
from utils.query_parser import extract_sql_query
from sql_chart.fetch_relationship import get_table_relations
def find_best_match_from_master_table(user_query):
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Folder containing this script
    file_path = os.path.join(script_dir, "table_metadata.json")
# Load master_output.json and prepare text data
    with open(file_path, "r") as f:
        master_data = json.load(f)

    """Finds the best matching tables for the user prompt using OpenAI."""
    
    system_prompt = "You are an AI assistant specialized in understanding table metadata and finding the best matching tables for a given user query. Your task is to analyze the table metadata and return the most relevant table names in an array of strings format based on the user's query. Be precise and return only the table names in the response."
    user_prompt = f"""
I have a list of database tables with detailed metadata about their purpose and key fields. Based on the following user query, identify and return the best matching table names as an array of strings.

### Table Metadata:
{json.dumps(master_data, indent=2)}

### User Query:
"{user_query}"

### Task:
Analyze the table metadata and determine which tables are most relevant to the user query. Return the result in an array of strings containing the table names only.

**Example Response Format:**
["TableName1", "TableName2", "TableName3"]
"""
   
    try:
        response = generate_response(user_prompt, system_prompt)
        """Finds the best matching tables for the user prompt using OpenAI."""
        tables = json.loads(response)
        
        headers = fetch_records_from_header_table(tables)
 
        relations = get_table_relations(tables)

        sql_query_response = process_query_and_generate_sql_query(headers, user_query, relations)
        
        sql_query = extract_sql_query(sql_query_response)
        return {
            "tables": tables,
            "relations": relations,
            "sql_query": sql_query
        }
    except Exception as e:
        print(f"Error during OpenAI API call: {e}")
        return {"best_match": None, "reasoning": "Unable to process the query due to an error."}