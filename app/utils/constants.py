schema = {
    "EpiUsers": {
        "description": "Details of users in the system, including personal information, role-specific attributes, and system access permissions.",
        "columns": [
            "Id", "LoginUserName", "FirstName", "LastName", "Email", "Designation", "DateCreated", 
            "LastModified", "BirthDate", "Department", "TotalExperience", "TimeInCurrentRole", 
            "WorkShift", "Location", "Latitude", "Longitude", "City", "State", "Country", 
            "Region", "IsTrained", "IsDeleted", "IsDisabled", "AllowMobile", "AllowClient"
        ]
    },
    "GpsLog": {
        "description": "Logs of user interactions with the system, including screen details, control events, timestamps, and additional metadata.",
        "columns": [
            "Sequence", "GpsXml", "Machine", "UserId", "TapName", "ScreenName", "ControlName", 
            "ControlType", "EventName", "ControlId", "ControlData", "SPKey", "ParentName", 
            "ParentType", "ControlClientRect", "ControlScreenRect", "LabelRect", "ControlImage", 
            "ScreenImage", "CursorPos", "ClickPos", "Timestamp", "UniqueStepHashcode", 
            "WindowsProcessId", "MainWindowHandle", "Sentence", "HashCode", 
            "FirstEventInSession", "LastEventInSession", "HideInGraph", "BlockId", 
            "SubSessionId", "AliasName", "Guid", "GpsFile", "ExtraInfo", "TabName", 
            "GridSelectedRow", "GridSelectedColumn", "FileRepositoryGUID", 
            "NumberOfDatapoints", "NumberOfPreRequisites", "NumberOfValidations", 
            "NumberOfExceptions", "IsNavigationStep", "IsInputStep", "IsStructuredData", 
            "ContainerId", "CanAutomatable", "AutomatibilityRate", "IsStrayStep", 
            "StepDuration", "AdaptorID", "StepId", "VPEDXml", "ApplicationURL"
        ]
    },
    "relationships": {
        "EpiUsers.Id": "GpsLog.UserId"
    }
}