from fastapi import APIRouter
from app.services.database import get_database_schema, fetch_data
from app.services.entities_actions_extractor import extract_entities_and_actions
from app.services.query_generator import generate_sql_query
from app.utils.query_parser import extract_sql_query
from pydantic import BaseModel
from fuzzywuzzy import fuzz
import json
import os

from app.sql_chart.fetch_master_tables import find_best_match_from_master_table

router = APIRouter()

unresolved_file_path = os.path.join(os.path.dirname(__file__), '../../collections/unresolved_queries.json')

class Prompt(BaseModel):
    query: str
@router.post("/prompts/sql-query-prompt")
async def process_prompt(prompt: Prompt):
    """
    Process a user query prompt and return the generated SQL and fetched data.
    """
    try:
        extracted_tables = find_best_match_from_master_table(prompt.query)
        print('extracted tables: ', extracted_tables)
        return extracted_tables
    except Exception as e:
        print(f"Error processing prompt: {e}")
        return {"success": False, "message": str(e)}