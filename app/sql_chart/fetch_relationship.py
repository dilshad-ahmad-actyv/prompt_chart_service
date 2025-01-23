import json
import os
def get_table_relations(tables=[]):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'table_relationships.json')
    with open(file_path, 'r') as f:
        data = json.load(f)
        
        tables = [item for item in tables]
        
        relations = [relation for relation in data if relation['ParentTable'] in tables or relation['ReferencedTable'] in tables]
    return relations