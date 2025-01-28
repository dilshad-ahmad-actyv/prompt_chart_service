import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql_chart.model_config import generate_response

def generate_summary(data, user_query, model):
    system_prompt = (
        "You are an expert in data analysis and summarization. Your task is to generate a concise and insightful summary "
        "of the provided data based on the user's query. The summary should help the user understand the data, its key characteristics, "
        "and performance metrics. Ensure the summary meets the following requirements:\n\n"
        "1. **Overview of the Data:** Provide a brief description of the data, such as its structure, types of fields, and notable patterns.\n"
        "2. **Comparative Insights:** Highlight comparisons within the data, such as maximum and minimum values, averages, trends, or outliers.\n"
        "3. **Performance Analysis:** If applicable, explain performance-related insights, such as how well certain entities, categories, or metrics are performing.\n\n"
        "### Context Data:\n"
        f"{json.dumps(data, indent=2)}\n\n"
        "### User Query:\n"
        f'"{user_query}"\n\n'
        "### Task:\n"
        "1. Analyze the data and query to identify the key areas of focus.\n"
        "2. Generate a human-readable summary that adheres to the guidelines provided above.\n"
        "3. The summary must be clear, concise, and tailored to the user's query, ensuring it is insightful and actionable.\n\n"
        "**Response Format:**\n"
        "Provide a structured summary in the following format:\n\n"
        "```\n"
        "### Summary:\n"
        "- **Data Overview:** (Brief description of the data)\n"
        "- **Comparative Insights:** (Key comparisons, trends, or outliers)\n"
        "- **Performance Analysis:** (Insights on performance or related metrics)\n"
        "```\n"
        "Ensure the output contains no additional explanations or unrelated details."
    )
    
    user_prompt = f"""Generate a summary based on the provided data and user query.

### Context Data:
{json.dumps(data, indent=2)}

### User Query:
"{user_query}"
"""
    
    response = generate_response(system_prompt, user_prompt, model)
    return response
