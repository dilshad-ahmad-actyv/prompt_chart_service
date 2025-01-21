import json
import requests  # For making API calls
from openai import OpenAI
# # DeepSeek API endpoint (replace with the actual endpoint)
# DEEPSEEK_API_URL = "https://api.deepseek.com/generate_metadata"
client = OpenAI(api_key="sk-adb871a1db8a4d2a969b91772056aec1", base_url="https://api.deepseek.com")
# Function to call DeepSeek API and generate metadata
def generate_metadata_with_deepseek(table_name, columns):
    print('table_name', table_name)
    print('columns', columns)
    """
    Calls the DeepSeek API to generate metadata for a table.
    :param table_name: Name of the table.
    :param columns: List of columns in the table.
    :return: Generated metadata as a string.
    """
    # Prepare the payload for the API call
    payload = {
        "table_name": table_name,
        "columns": columns
    }

    messages =     [{
        "role": "system",
        "content": """Input:
Provide the JSON data for the table, including the header, table, type, data, and metadata fields for each column.

Output Format:
"The [table] table stores [general purpose], including [specific details about the table's role or function]. Key fields include: [Field1] ([short description]), [Field2] ([short description]), and [Field3] ([short description])."""
    },
    {
        "role": "user",
        "content": f"{json.dumps(payload)}",
    }]
    # Make the API call
    try:
        response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False
        )

        if not response.choices or not response.choices[0].message.content:
            # logging.warning("Response received, but no content was found.")
            return "No response generated. Please try again."

        return response.choices[0].message.content.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling DeepSeek API for table {table_name}: {e}")
        return f"Metadata generation failed for table {table_name}."


with open ('master_output.json', 'r') as master_output:
    tables = json.load(master_output)
# Generate metadata for each table using DeepSeek API
table_metadata = {}
for table_name, columns in tables.items():
    # Extract column names and metadata for the API call
    column_info = [{"header": col["header"], "metadata": col["metadata"]} for col in columns]
    print(f'-------------------{column_info}-----------------------')
    # Call DeepSeek API to generate metadata for the table
    metadata = generate_metadata_with_deepseek(table_name, column_info)
    
    # Store the generated metadata
    table_metadata[table_name] = metadata
    with open('table_metadata.json', 'w') as metadata_file:
        json.dump(table_metadata, metadata_file, indent=4)

print("Metadata generation completed. Check 'table_metadata.json' for the output.")

# Write the metadata to a new JSON file