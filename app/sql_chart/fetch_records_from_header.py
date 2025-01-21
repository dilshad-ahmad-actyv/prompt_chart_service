import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

from utils.query_parser import extract_sql_query
from sql_chart.model_config import generate_response
def fetch_records_from_header_table(table_names):
 
    """Fetch records corresponding to the specified tables from master_output.json."""
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Folder containing this script
    file_path = os.path.join(script_dir, "master_output.json")

    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    tables = [table.lower() for table in table_names]
    records = [{table_name: value} for table_name, value in data.items() if table_name.lower() in tables]

    # print('Records ', records)
    return records