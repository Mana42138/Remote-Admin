---

## Welcome to the Remote Admin Tool

### Overview

Welcome! I created this tool as a solution for remote administration and interaction across multiple PCs on a network. This program is designed to work collaboratively with other computers and should be used responsibly and ethically. It’s important to note that it is not intended for any malicious activities.

### Purpose

I developed this tool because I was looking for a way to manage networked computers without needing to deal with the complexities of socket port forwarding.

### Features

This Remote Admin Tool uses an API to facilitate interactions between a server and multiple client PCs. Each connected PC appears as a separate entry in a table on the server interface, allowing you to manage and interact with each machine as long as the program is running on the client PC.

### Setup Instructions

**⚠️ SETUP WARNING ⚠️**

When you run `setup.bat` on any PC, it configures that PC as a client (referred to as a "zombie"). Make sure to update the `SCRIPT_URL` variable in the `.bat` file to point to your server before distributing it.

### How to Use

- **`setup.bat`**: Provide this script to the user who will execute it to connect their PC to your server. (Note: The client PC will send requests to your server upon reboot.)

- **`Client.py`**: This is the script you will run to interact with the PCs that are connected to the server.

- **`main.py`**: This is the server script that handles all incoming requests. I’ve used Flask for its simplicity and ease of use, though other frameworks might offer different features.

### Installation

Python and the required packages will be installed automatically during the setup process!

### Q&A
----
Q: Why do you only use GET requests?

A: I use GET requests because some computers have restrictions that prevent POST requests from working properly. To avoid these compatibility issues, I opted for GET requests.
---

all though you could just use a ssh server now that i think about it oh well :)
