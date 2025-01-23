import json
tables = ['MigrationId', 'RoleId', 'JobId', 'AgentId', 'EventId', 'CaptureJobId', 'CapturePreferenceId', 'CaptureResourceGroupId', 'ProjectId', 'GroupId', 'PIUserGroupId', 'UserId', 'GenieScriptId', 'MachineId', 'RPAUserGroupId', 'GenieJobId', 'ProcessTaskId', 'StepId', 'GWZFileGUID', 'ApplicationVaultId', 'MachineGroupId', 'OSVaultId', 'OperationId', 'SlNo', 'ProcessFileId', 'CabFileID']
with open('table_relationships.json', 'r') as f:
    data = json.load(f)
    
    parent_columns = {entry['ParentColumn'] for entry in data}
    referenced_columns = {entry['ReferencedColumn'] for entry in data}

    res = [table for table in tables if table not in parent_columns]
    print(res)