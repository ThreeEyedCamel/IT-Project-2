import sqlite3
import hashlib
import socket
import threading
import re
from tkinter import *
import tkinter as tk
import mazeEditorTkinter

# Event object for stopping thread
event_obj = threading.Event()

# Global variable to keep track of the current Tk instance
current_window = None

def destroy_current_window():
    """Destroy the current Tk window if it exists."""
    global current_window
    if current_window:
        current_window.destroy()
        current_window = None

# Setting up the userdata database
def security_setup():
    """Initialize the database and populate it with sample user data."""
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS userdata (
                    id INTEGER PRIMARY KEY,         
                    username VARCHAR(255) NOT NULL, 
                    password VARCHAR(255) NOT NULL
                    )""")
    username_passwords = [
        ('User1', 'password1234!'),
        ('User2', 'password2234!'),
        ('User3', 'password3234!'),
        ('User4', 'password4234!'),
        ('User5', 'password5234!')
    ]
    for username, password in username_passwords:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)", (username, hashed_password))
    conn.commit()
    cur.execute("SELECT * FROM userdata")
    result = cur.fetchall()
    print(result)
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

def update_userdata(username, password):
    """Update the user database with new credentials."""
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS userdata (
                    id INTEGER PRIMARY KEY,         
                    username VARCHAR(255) NOT NULL, 
                    password VARCHAR(255) NOT NULL
                    )""")
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)", (username, hashed_password))
    conn.commit()
    conn.close()

def handle_connection(c):
    """Handle incoming connections and user credentials."""
    def on_submit():
        username = inputUser.get("1.0", "end-1c").strip()
        password = inputP1.get("1.0", "end-1c").strip()
        connection_result(c, username, password)

    global current_window
    destroy_current_window()
    
    current_window = Tk()
    current_window.title("Set Credentials")
    current_window.geometry("500x500+50+50")

    Label(current_window, text="Login").pack()
    Label(current_window, text="Username:").place(relx=0.5, rely=0.05, anchor='n')
    Label(current_window, text="Password:").place(relx=0.5, rely=0.2, anchor='n')

    inputUser = tk.Text(current_window, height=2, width=20)
    inputP1 = tk.Text(current_window, height=2, width=20)
    
    inputUser.place(relx=0.5, rely=0.1, anchor='n')
    inputP1.place(relx=0.5, rely=0.25, anchor='n')

    submitButton = tk.Button(current_window, text="Submit", command=on_submit)
    submitButton.place(relx=0.5, rely=0.6, anchor='n')

    current_window.mainloop()
    c.close()

def connection_result(c, username, password):
    """Process and display the result of the login attempt."""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
    result = cur.fetchall()
    conn.close()
    
    msg = "Login successful!" if result else "Login FAILED"
    
    global current_window
    destroy_current_window()

    current_window = Tk()
    Label(current_window, text=msg).pack()
    c.send(msg.encode())
    current_window.mainloop()

    if result:
        app = mazeEditorTkinter.MazeEditor()
        app.mainloop()

def client():
    """Client function to connect and interact with the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 9999))

    message = client_socket.recv(1024).decode()
    client_socket.send(input(message).encode())

    message = client_socket.recv(1024).decode()
    client_socket.send(input(message).encode())

    print(client_socket.recv(1024).decode())

def start_server():
    """Start the server to accept client connections."""
    print("Server is listening...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,)).start()

def main():
    """Start the server and client communication."""
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    client()

def has_numbers(string):
    """Check if the string contains any numbers."""
    return bool(re.search(r'\d', string))

def special_characters(string):
    """Check if the string contains special characters."""
    characters = "!@#$%^&*()-+?_=,<>/"
    return any(i in characters for i in string)

def first_window():
    """Display the first window with options to set credentials or log in."""
    global current_window
    destroy_current_window()
    
    current_window = Tk()
    current_window.title("Choice")

    tk.Button(current_window, text="Set credentials", command=set_credentials).place(relx=0.5, rely=0.2, anchor='n')
    tk.Button(current_window, text="Login", command=main).place(relx=0.5, rely=0.4, anchor='n')

    current_window.mainloop()

def set_credentials():
    """Display the window to set new credentials."""
    global current_window
    destroy_current_window()
    
    current_window = Tk()
    current_window.title("Set Credentials")
    current_window.geometry("500x500+50+50")

    Label(current_window, text="Login").pack()
    Label(current_window, text="Username:").place(relx=0.5, rely=0.05, anchor='n')
    Label(current_window, text="Password:").place(relx=0.5, rely=0.2, anchor='n')
    Label(current_window, text="Re-enter password: ").place(relx=0.5, rely=0.35, anchor='n')
    Label(current_window, text="Password requirements:\n 10 characters long \n Contains numbers \n Contains a special character").place(relx=0.5, rely=0.8, anchor='n')

    inputUser = tk.Text(current_window, height=2, width=20)
    inputP1 = tk.Text(current_window, height=2, width=20)
    inputP2 = tk.Text(current_window, height=2, width=20)

    def on_submit():
        verify(inputUser.get("1.0", "end-1c").strip(), inputP1.get("1.0", "end-1c").strip(), inputP2.get("1.0", "end-1c").strip())
        
    tk.Button(current_window, text="Submit", command=on_submit).place(relx=0.5, rely=0.6, anchor='n')

    inputUser.place(relx=0.5, rely=0.1, anchor='n')
    inputP1.place(relx=0.5, rely=0.25, anchor='n')
    inputP2.place(relx=0.5, rely=0.4, anchor='n')

    current_window.mainloop()

def verify(user, pass1, pass2):
    """Verify the credentials and show result."""
    global current_window
    destroy_current_window()
    
    current_window = Tk()
    if pass1 == pass2 and len(pass1) >= 10 and has_numbers(pass1) and special_characters(pass1):
        update_userdata(user, pass1)
        Label(current_window, text="Credentials added").pack()
    else:
        Label(current_window, text="Password doesn't meet requirements").pack()

    current_window.mainloop()

if __name__ == "__main__":
    first_window()
