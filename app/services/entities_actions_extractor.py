import openai
from config.settings import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

# def extract_entities_and_actions(prompt, schema):
#     # Format the schema description for OpenAI
#     schema_description = "\n".join(
#         f"Table: {table}, Columns: {', '.join(columns)}"
#         for table, columns in schema.items()
#     )

#     # System message: define the assistant's behavior and purpose
#     system_message = (
#         "You are a highly skilled assistant that extracts entities (tables and columns) and actions "
#         "from user prompts based on the database schema provided. "
#         "Your goal is to analyze the user's request, identify relevant tables and columns (entities), "
#         "and determine the action (e.g., SELECT, INSERT, UPDATE, DELETE). "
#         "Here is the database schema:\n"
#         f"{schema_description}\n"
#         "Always use this schema to ensure that the entities and actions you provide are valid."
#         "Try and analize all possible tables and columns which suites the  user's prompt"
#         "Make sure that COLUMNS should be matched with TABLE based on the SCHEMA provided."
#         "If you cannot find a match in the schema for the user's prompt, "
#         "respond with 'The schema does not support this request.'"
#     )

#     # system_message = (
#     # "You are a highly intelligent and schema-aware assistant. Your task is to extract entities (tables and their respective columns) "
#     # "and actions (e.g., SELECT, INSERT, UPDATE, DELETE) from complex user prompts by analyzing the provided database schema. "
#     # "You must ensure that:\n"
#     # "1. Columns are strictly associated with their respective tables as defined in the schema.\n"
#     # "3. Synonyms, antonyms, and linguistic variations in the user's prompt are used to infer intent, but the table and columns should be correct and matched with schema.\n\n"
#     # "Instructions:\n"
#     # "- Use the schema to match tables and columns accurately, respecting case sensitivity.\n"
#     # "- Ensure that the output explicitly maps tables to their columns.\n"
#     # "- If the schema does not support the user's request, respond with: 'The schema does not support this request.'\n"
#     # "Focus on accuracy, schema alignment, and clarity in your response.\n"
#     # "Here is the database schema:\n"
#     # f"{schema_description}\n\n"
#     # )


#     # User message: specify the user's prompt
#     user_message = (
#     f"User Prompt: {prompt}\n\n"
#     "Based on the provided database schema, identify the relevant tables and columns (entities) and actions required to fulfill the user's request. "
#     "Respond in the following structured format:\n\n"
#     "  Entities:\n"
#     "    TableName1: [Column1, Column2, ...]\n"
#     "    TableName2: [Column1, Column2, ...]\n"
#     "  Actions: [Action1, Action2, ...]\n\n"
#     "Here is the database schema:\n"
#     f"{schema_description}\n\n"
#     )


#     # OpenAI API call to extract entities and actions
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": system_message},
#             {"role": "user", "content": user_message},
#         ]
#     )

#     print('-------------------response-------------->', response)
#     # Parse the response
#     response_content = response['choices'][0]['message']['content']
#     return response_content


import openai

# Define your OpenAI API key
openai.api_key = "your_openai_api_key"

def extract_entities_and_actions(prompt, schema):
    """
    Uses OpenAI GPT-4 to extract user intent, questions, and relationships from a natural language query.
    
    Parameters:
        prompt (str): The user's natural language query.
        schema (Dict): The database schema containing table descriptions, columns, and relationships.
    
    Returns:
        Dict: A dictionary with extracted intent, questions, and relationships.
    """
    # Prepare schema context for OpenAI
    schema_context = "Database Schema:\n"
    for table, details in schema.items():
        schema_context += f"- Table: {table}\n  Description: {details.get('description', '')}\n  Columns: {', '.join(details.get('columns', []))}\n"
    if "relationships" in schema:
        schema_context += "Relationships:\n"
        for col1, col2 in schema["relationships"].items():
            schema_context += f"  {col1} -> {col2}\n"

    # Prompt for OpenAI
    gpt_prompt = f"""
You are a database assistant. Use the following schema to extract user intent, questions, and relationships:
{schema_context}
User Query:
"{prompt}"

Provide the result as a JSON object with the following keys:
- intent: The user's intent (e.g., "Retrieve Data", "Count Data", "Update Data").
- questions: A list of main questions from the user's query.
- tables: A list of table names referenced in the query.
- columns: A list of columns referenced in the query.
- conditions: A list of conditions (filters) implied by the query.
- relationships: A list of relationships involved (if applicable).
- use relationship but extract name (Concatenate FirstName and LastName if it's in the query string.) of the user as per columns, instead of using userId
"""

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Specify GPT-4 model
        messages=[{"role": "system", "content": "You are an advanced database assistant."},
                  {"role": "user", "content": gpt_prompt}],
        # max_tokens=500,
        temperature=0.2  # Low temperature for deterministic results
    )

    # Parse and return the result
    try:
        result = eval(response['choices'][0]['message']['content'].strip())  # Convert GPT's JSON-like response into Python dict
    except Exception as e:
        result = {"error": f"Failed to parse GPT response: {e}"}
    
    return result

# Example schema

# # Example prompt
# user_prompt = "Find all users who are allowed mobile access and logged into Salesforce."

# # Extract intent, questions, and relationships using GPT-4
# extracted_info = extract_intent_and_relationship_with_gpt4(user_prompt, schema)
# print("Extracted Information:")
# print(extracted_info)
