from pathlib import Path
import json

# def checkUser():
#     userId = "Tester"
#     return userId

def loadPermissions():
    BASE_DIR = Path(__file__).resolve().parents[2]      
    json_path = BASE_DIR /"src" / "config" / "llmConfig.json"      

    with json_path.open("r", encoding="utf-8") as f:
        allowedUsers = json.load(f)
    return allowedUsers

def validateUser(user_id):
    userId = user_id
    allowedUsers = loadPermissions()
    permissions = allowedUsers["allowedUsers"]
    if userId in permissions:
        return True, userId
    else:
        return False, userId
    
