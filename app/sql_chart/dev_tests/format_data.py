import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
# Function to generate metadata dynamically using OpenAI
from sql_chart.model_config import generate_response
def generate_metadata(column_name, table_name, column_data):
    # Prepare the prompt with column name, table name, and sample data
    
      # Prepare a preview of the sample data as a comma-separated string
   # Take the first 5 records and sanitize items
    sample_data_preview = column_data[:]
   # Sanitize each item in the preview
    sanitized_preview = []
    for item in sample_data_preview:
        if isinstance(item, dict):
            # Convert dictionaries to a readable format
            sanitized_preview.append(json.dumps(item))
        elif isinstance(item, list):
            # Convert lists to a readable format
            sanitized_preview.append(", ".join(map(str, item)))
        else:
            # Use the item as is for simple types
            sanitized_preview.append(str(item))

    # Join sanitized items into a single string
    sample_data_preview = ", ".join(sanitized_preview)
    # print('sample_data_preview: ', type(sample_data_preview))
    prompt = f"""
    You are a data analyst tasked with generating metadata for a database column. Using the given table name, column name, and sample data, create a concise description of what the column represents.

    Context:
    - **Table Name:** {table_name}
    - **Column Name:** {column_name}
    - **Sample Data:** '{sample_data_preview}'

    Guidelines:
    1. Clearly describe the purpose or role of the column in the context of the table.
    2. Mention the type of information stored (e.g., identifier, name, status, etc.).
    3. Use the sample data to provide hints about its possible use or meaning.
    4. Be concise and specific in your description.

    Provide your response in one or two sentences.
    """

    # print('prompt ------->', prompt)
    try:
        # Query OpenAI's API to generate metadata
        system_prompt = "You are a helpful assistant that generates metadata for database columns."
        metadata = generate_response(prompt, system_prompt)
    except Exception as e:
        
        # print('prompt ------->', prompt)
        metadata = f"Error generating metadata: {str(e)}"

    return f"{metadata}"

# Mapping of Python data types to descriptive strings
type_mapping = {
    str: "string",
    int: "number",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    None: "null",
    type(None): "null"
}

# Function to get the string representation of a type
def python_type_to_string(py_type):
    return type_mapping.get(py_type, "unknown")  # Default to 'unknown' if type is not mapped

# Function to infer the type of data dynamically
def infer_type(column_name):
    return python_type_to_string(type(column_name))

# Function to process the schema and generate the output
def process_schema(schema_file):
    with open(schema_file, 'r') as file:
        schema = json.load(file)

    result = []
    for table in schema:
        table_name = table.get("table", "UnknownTable")
        columns = table.get("columns", [])
        table_data = table.get("data", [])
        for column in columns:
                        # Extract data for this column from the table data
            column_data = [row.get(column, None) for row in table_data]
            result.append({
                "header": column,
                "table": table_name,
                "type": infer_type(column),
                # "data": column_data,
                "metadata": generate_metadata(column, table_name, column_data)
            })

    # print('result------->', result)
    return result

# Main execution
if __name__ == "__main__":
    schema_file = "schema.json"  # Replace with your schema file name
    output = process_schema(schema_file)

    # Write to a new JSON file or print it
    with open("output.json", "w") as output_file:
        json.dump(output, output_file, indent=2)

    print("Metadata generation completed. Output written to 'output.json'.")
