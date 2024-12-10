from fastapi import APIRouter
import json
import os

router = APIRouter()

file_path = os.path.join(os.path.dirname(__file__), '../../collections/unresolved_queries.json')

@router.get('/prompts/unresolved-queries')
def unresolved_queries():
    with open (file_path, 'r') as file:
        unresolved_queries = json.load(file)
        return unresolved_queries