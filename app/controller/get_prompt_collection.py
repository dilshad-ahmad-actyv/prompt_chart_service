from fastapi import APIRouter
import json
import os

router = APIRouter()
file_path = os.path.join(os.path.dirname(__file__), '../../collections/schema.json')
print('file_path,', file_path)

@router.get('/prompts')
async def get_prompt_collections():
    
    with open(file_path, 'r') as file:
        data = json.load(file)
        prompt_collections = [item['prompt'] for item in data]
    return prompt_collections