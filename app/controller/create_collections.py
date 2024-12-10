from fastapi import APIRouter, HTTPException
import json
import os

file_path = os.path.join(os.path.dirname(__file__), '../../collections/schemas.json')

router = APIRouter()

@router.post('/prompts')
def create_prompt_collection(prompt_collection: dict):
    """
    Add a new prompt collection to the JSON file.
    """
    try:
        # Read existing data
        if not os.path.exists(file_path):
            # Initialize the file if it doesn't exist
            data = []
        else:
            with open(file_path, 'r') as f:
                data = json.load(f)

        # Append the new prompt collection
        data.append(prompt_collection)

        # Write back to the file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

        return {"success": True, "message": "Prompt collection added successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
