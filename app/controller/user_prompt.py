from fastapi import APIRouter
from app.services.database import get_database_schema, fetch_data
from app.services.entities_actions_extractor import extract_entities_and_actions
from app.services.query_generator import generate_sql_query
from app.utils.query_parser import extract_sql_query
from pydantic import BaseModel
from fuzzywuzzy import fuzz
import json
import os

from app.utils.constants import schema

router = APIRouter()

unresolved_file_path = os.path.join(os.path.dirname(__file__), '../../collections/unresolved_queries.json')

class Prompt(BaseModel):
    query: str
@router.post("/prompts/search-query")
async def process_prompt(prompt: Prompt):
    """
    Process a user query prompt and return the generated SQL and fetched data.
    """
    
    try:
        sql_query = None
        response = searchPromptInPreDefinedCollection(prompt.query)
        print('PreDefined response', response)
        print('SQL query....', sql_query)
        if response:
            sql_query = response['sql']
            # return response
        else:
            print('-------------------Before--------------------------')
            # Store prompts as unresolved query in unresolved collection 
            with open(unresolved_file_path, 'r') as f:
                unresolved_queries = json.load(f)
                unresolved_queries.append({"prompt": prompt.query, "ms_sql": ''})
                with open(unresolved_file_path, 'w') as f:
                    json.dump(unresolved_queries, f, indent=4)
            print('-------------------Before--------------------------', sql_query) 
            # Process to generate sql query using schema, prompts and LLM
            sql_query = generateNewQuery(prompt)
            #Fetch data from the database
        
        data = fetch_data(sql_query)
        print('data------------>', data)
        return {
            "success": True,
            "sql_query": sql_query,
            "data": data,
        }
    except Exception as e:
            return {"success": False, "error": str(e)}

def searchPromptInPreDefinedCollection(prompt, threshold=95):
    # Path to the schema.json file
    file_path = os.path.join(os.path.dirname(__file__), '../../collections/schema.json')
    print ("Searching...", prompt)
    try:
        # Open and load JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Perform fuzzy search
        for item in data:
            similarity = fuzz.ratio(prompt.lower(), item.get("prompt", "").lower())
            if similarity >= threshold:
                return {
                    "matched_prompt": item.get("prompt"),
                    "similarity": similarity,
                    "sql": item.get("ms_sql")
                }
        
        # If no match found
        print({"message": "No prompt matches the threshold.", "similarity": 0})
        return None
    except FileNotFoundError:
        return {"error": f"File not found at {file_path}"}
    except json.JSONDecodeError:
        return {"error": f"Malformed JSON in {file_path}"}


def generateNewQuery(prompt):
    # TODO: Implement this function to generate a new SQL query based on the user's prompt
    # schema = get_database_schema()
    print('schema: ', schema)
    entities_actions = extract_entities_and_actions(prompt.query, schema)
    print('entities_actions: ', entities_actions)
    # sql_query = generate_sql_query(prompt.query, schema, entities_actions)
    sql_query = generate_sql_query(prompt.query, entities_actions)
    print('sql_query: ', sql_query)
    extracted_query = extract_sql_query(sql_query)
    
    return extracted_query