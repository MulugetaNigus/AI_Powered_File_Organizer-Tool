import requests
import json
import os
import dotenv
import logging

dotenv.load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define your tool functions (from watch_file.py)
def listInCurrrentDirectory():
    return os.listdir('./')

def findFolder(folderName):
    if os.path.exists(folderName.lower()):
        return os.listdir(folderName.lower())
    else:
        return "Folder not found"

def navigateToFolder(folderName):
    try:
        os.chdir(folderName)
        return f"Navigated to {folderName}"
    except Exception as e:
        return f"Failed to navigate: {str(e)}"

def createFolder(folderName):
    os.makedirs(folderName, exist_ok=True)
    return "Folder created"

def copyFiles(file, folderName):
    import shutil
    shutil.copy(file, folderName)
    return "File copied"

# Function to call tools based on AI response
def call_tool(function_name, arguments):
    if function_name == "listInCurrrentDirectory":
        return listInCurrrentDirectory()
    elif function_name == "createFolder":
        createFolder(arguments.get("folderName"))
        return "Folder created"
    elif function_name == "copyFiles":
        copyFiles(arguments.get("file"), arguments.get("folderName"))
        return "File copied"
    elif function_name == "findFolder":
        return findFolder(arguments.get("folderName"))
    elif function_name == "navigateToFolder":
        return navigateToFolder(arguments.get("folderName"))
    else:
        return "Unknown tool"
def chat_with_tools(user_message):
    logging.info(f"User Message: {user_message}")
    messages = [
        {
            "role": "user",
            "content": user_message
        }
    ]
    
    while True:  # Loop for tool calls
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "x-ai/grok-4-fast:free",
                "messages": messages,
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": "listInCurrrentDirectory",
                            "description": "Lists all files and folders in the current directory.",
                            "parameters": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "navigateToFolder",
                            "description": "Navigates to the specified folder, changing the current working directory.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "folderName": {
                                        "type": "string",
                                        "description": "The name or path of the folder to navigate to."
                                    }
                                },
                                "required": ["folderName"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "createFolder",
                            "description": "Creates a new folder with the given name.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "folderName": {
                                        "type": "string",
                                        "description": "The name of the folder to create."
                                    }
                                },
                                "required": ["folderName"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "copyFiles",
                            "description": "Copies a file to the specified folder.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "file": {
                                        "type": "string",
                                        "description": "The path of the file to copy."
                                    },
                                    "folderName": {
                                        "type": "string",
                                        "description": "The folder to copy the file into."
                                    }
                                },
                                "required": ["file", "folderName"]
                            }
                        }
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "findFolder",
                            "description": "Finds a folder with the given name.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "folderName": {
                                        "type": "string",
                                        "description": "The name of the folder to find."
                                    }
                                },
                                "required": ["folderName"]
                            }
                        }
                    }
                ],
                "tool_choice": "auto"  # Let the model decide when to use tools
            })
        )
        
        res = response.json()
        message = res["choices"][0]["message"]
        
        # Log AI thinking
        if message.get("content"):
            logging.info(f"AI Thinking: {message['content']}")
        
        # Add the AI's response to messages
        messages.append(message)
        
        # Check for tool calls
        if "tool_calls" in message:
            for tool_call in message["tool_calls"]:
                function_name = tool_call["function"]["name"]
                arguments = json.loads(tool_call["function"]["arguments"])
                logging.info(f"Tool Call: {function_name} with args: {arguments}")
                tool_result = call_tool(function_name, arguments)
                logging.info(f"Tool Result: {tool_result}")
                
                # Add tool result back to messages
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(tool_result)
                })
        else:
            # No more tools, return final response
            logging.info(f"Final Response: {message['content']}")
            return message["content"]


user_input = input("How do you want organize your files and tell me which folders you want me to watch for file organizations?: ")
result = chat_with_tools(user_input)
print(result)