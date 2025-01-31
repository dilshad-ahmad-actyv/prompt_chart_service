import sys
import os
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sql_chart.model_config import generate_response
 
def generate_summary(data, user_query, model):
    system_prompt = """You are an expert in data analysis and summarization. Your task is to generate a concise and insightful summary "
        "of the provided data based on the user's query. The summary should help the user understand the data, its key characteristics, "
        "and performance metrics. **Additionally**, based on the data, you must also:\n\n"
        "1. Identify the ideal type of chart for the data based on common use cases:\n"
        "   - **Bar chart** for comparing multiple categories (e.g., different users, products).\n"
        "   - **Line chart** for data points spanning a duration of time (e.g., daily or weekly metrics).\n"
        "   - **Pie chart** if there is a single entity with several subdivisions (e.g., tasks or categories for one user).\n\n"
        "2. Infer and rename columns to more human-friendly axis labels when presenting the data:\n"
        "   - For instance, if you see a column named 'duration', rename it to 'Time (sec)'.\n"
        "   - If you see a column named 'epiusers', rename it to 'User (name)'.\n"
        "   - Apply similar intuitive label transformations to other columns where applicable.\n\n"
        "### Context Data:\n"
        f"{json.dumps(data, indent=2)}\n\n"
        "### User Query:\n"
        f'"{user_query}"\n\n"
        "### Task:\n"
        "1. Analyze the data and query to identify the key areas of focus.\n"
        "2. Generate a human-readable summary that adheres to the guidelines provided above.\n"
        "3. The summary must be clear, concise, and tailored to the user's query, ensuring it is insightful and actionable.\n"
        "4. Propose the most appropriate chart type, along with any recommended axis labels.\n\n"
        "**Response Format:**\n"
        "Provide a structured summary in the following format:\n\n"
        "```\n"
        "## Response\n"
        "**Data Retrieved \n add the context data here in a list format**\n"
        "- **Overview\n** (Brief description of the data)\n"
        "- **Comparative Insights \n** (Key comparisons, trends, or outliers)\n"
        "- **Performance Analysis \n** (Insights on performance or related metrics)\n"
        "- **Recommended Chart Type \n** (Bar, Line, or Pie, with short explanation why)\n"
        "- **Axis Labels (if applicable) \n** (Proposed x-axis and y-axis labels or pie chart labels)\n"
        "```\n"
        "Ensure the output contains no additional explanations or unrelated details."""

 
    user_prompt = f"""Generate a summary based on the provided data and user query.
 
### Context Data:
{json.dumps(data, indent=2)}
 
### User Query:
"{user_query}"
"""
 
    response = generate_response(system_prompt, user_prompt, model)
    return response





# import sys
# import os
# import json
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# from sql_chart.model_config import generate_response

# def generate_summary(data, user_query, model):
#     system_prompt = (
#         "You are an expert in data analysis and summarization. Your task is to generate a concise and insightful summary "
#         "of the provided data based on the user's query. The summary should help the user understand the data, its key characteristics, "
#         "and performance metrics. Ensure the summary meets the following requirements:\n\n"
#         "1. **Overview of the Data:** Provide a brief description of the data, such as its structure, types of fields, and notable patterns.\n"
#         "2. **Comparative Insights:** Highlight comparisons within the data, such as maximum and minimum values, averages, trends, or outliers.\n"
#         "3. **Performance Analysis:** If applicable, explain performance-related insights, such as how well certain entities, categories, or metrics are performing.\n\n"
#         "### Context Data:\n"
#         f"{json.dumps(data, indent=2)}\n\n"
#         "### User Query:\n"
#         f'"{user_query}"\n\n'
#         "### Task:\n"
#         "1. Analyze the data and query to identify the key areas of focus.\n"
#         "2. Generate a human-readable summary that adheres to the guidelines provided above.\n"
#         "3. The summary must be clear, concise, and tailored to the user's query, ensuring it is insightful and actionable.\n\n"
#         "**Response Format:**\n"
#         "Provide a structured summary in the following format:\n\n"
#         "```\n"
#         "## Summary:\n"
#         "**Output: add the context data here as table format\n"
#         "- **Data Overview:** (Brief description of the data)\n"
#         "- **Comparative Insights:** (Key comparisons, trends, or outliers)\n"
#         "- **Performance Analysis:** (Insights on performance or related metrics)\n"
#         "```\n"
#         "Ensure the output contains no additional explanations or unrelated details."
#     )
    
#     user_prompt = f"""Generate a summary based on the provided data and user query.

# ### Context Data:
# {json.dumps(data, indent=2)}

# ### User Query:
# "{user_query}"
# """
    
#     response = generate_response(system_prompt, user_prompt, model)
#     return response
