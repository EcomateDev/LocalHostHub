import tkinter as tk
from tkinter import filedialog
import subprocess
import http.server
import socketserver
import threading
import time
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/file-info':
            # Send information about the current file to the control_panel.html page
            response = {
                'currentFile': current_file
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        elif self.path == '/server-status':
            # Send information about the server status to the control_panel.html page
            response = {
                'serverStatus': server_status
            }
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

# Variables to store information about the running file and server status
current_file = "File not defined"
server_status = "Server not running"

# Function to run a file
def run_file():
    global current_file
    file_path = filedialog.askopenfilename()
    if file_path:
        current_file = file_path
        if file_path.endswith((".py", ".cpp", ".c", ".java", ".js")):
            # If it's code, run it
            subprocess.Popen(["python", file_path], shell=True)
        else:
            # Otherwise, open the file with the default program
            subprocess.Popen(["start", file_path], shell=True)

# Function to start the server
def start_server():
    global server_status
    server_status = "Server is running"
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("localhost", 8000), handler) as httpd:
        httpd.serve_forever()

# Start the server in a separate thread
server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

# Create a Tkinter window
root = tk.Tk()
root.title("Run File and Server")

# Create a button to choose a file and run it
select_button = tk.Button(root, text="Choose a File", command=run_file)
select_button.pack()

# Function to update the display information
def update_display():
    file_info_label.config(text=f"Running file: {os.path.basename(current_file)}")
    status_label.config(text=f"Server status: {server_status}")
    root.after(1000, update_display)

# Display information
file_info_label = tk.Label(root, text=f"Running file: {os.path.basename(current_file)}")
file_info_label.pack()
status_label = tk.Label(root, text=f"Server status: {server_status}")
status_label.pack()

# Start the Tkinter main loop
root.after(1000, update_display)
root.mainloop()
