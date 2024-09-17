import sqlite3
import hashlib
import socket
import threading
import re
from tkinter import *
import tkinter as tk
import mazeEditorTkinter

def gui():
    # Launch mazeEditorTkinter.MazeEditor
    app = mazeEditorTkinter.MazeEditor()
    app.mainloop()

def security_setup():
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY,         
                username VARCHAR(255) NOT NULL, 
                password VARCHAR(255) NOT NULL
                )
    """)

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
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY,         
                username VARCHAR(255) NOT NULL, 
                password VARCHAR(255) NOT NULL
                )
    """)

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)", (username, hashed_password))
    conn.commit()
    conn.close()

def handle_connection(c):
    print("connection handle")
    def on_submit():
        print("submit")
        username = inputUser.get(1.0, "end-1c")
        password = inputP1.get(1.0, "end-1c")
        connection_result(c, username, password)

    # Create a new Tkinter window for handling connection
    connection_window = Toplevel()
    connection_window.title("Login")
    connection_window.geometry("500x500+50+50")
    print("1")
    Label(connection_window, text="Login").pack()
    Label(connection_window, text="Username:").place(relx=0.5, rely=0.05, anchor='n')
    Label(connection_window, text="Password:").place(relx=0.5, rely=0.2, anchor='n')
    print("2")
    inputUser = tk.Text(connection_window, height=2, width=20)
    inputP1 = tk.Text(connection_window, height=2, width=20)
    print("3")
    inputUser.place(relx=0.5, rely=0.1, anchor='n')
    inputP1.place(relx=0.5, rely=0.25, anchor='n')
    print("4")
    submitButton = tk.Button(connection_window, text="Submit", command=on_submit)
    submitButton.place(relx=0.5, rely=0.6, anchor='n')
    print("5")
    connection_window.mainloop()
    c.close()
    print("6")

def connection_result(c, username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
    result = cur.fetchall()
    if result:
        msg = "Login successful!"
        gui()  # Close current and open the new application
    else:
        msg = "Login FAILED"

    result_window = Toplevel()
    Label(result_window, text=msg).pack()
    c.send(msg.encode())
    result_window.mainloop()

def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999))

    message = client.recv(1024).decode()
    client.send(input(message).encode())

    message = client.recv(1024).decode()
    client.send(input(message).encode())

    print(client.recv(1024).decode())

def start_server():
    print("Server is listening...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,)).start()

def main():
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    client()

def has_numbers(string):
    return bool(re.search(r'\d', string))

def special_characters(string):
    characters = "!@#$%^&*()-+?_=,<>/"
    return any(i in characters for i in string)

def first_window():
    global root
    root = Tk()
    root.title("Choice")

    tk.Button(root, text="Set credentials", command=set_credentials).place(relx=0.5, rely=0.2, anchor='n')
    tk.Button(root, text="Login", command=main).place(relx=0.5, rely=0.4, anchor='n')

    root.mainloop()

def set_credentials():
    credentials_window = Toplevel()
    credentials_window.title("Set Credentials")
    credentials_window.geometry("500x500+50+50")

    Label(credentials_window, text="Login").pack()
    Label(credentials_window, text="Username:").place(relx=0.5, rely=0.05, anchor='n')
    Label(credentials_window, text="Password:").place(relx=0.5, rely=0.2, anchor='n')
    Label(credentials_window, text="Re-enter password: ").place(relx=0.5, rely=0.35, anchor='n')
    Label(credentials_window, text="Password requirements:\n 10 characters long \n Contains numbers \n Contains a special character").place(relx=0.5, rely=0.8, anchor='n')

    inputUser = tk.Text(credentials_window, height=2, width=20)
    inputP1 = tk.Text(credentials_window, height=2, width=20)
    inputP2 = tk.Text(credentials_window, height=2, width=20)

    def on_submit():
        verify(inputUser.get(1.0, "end-1c"), inputP1.get(1.0, "end-1c"), inputP2.get(1.0, "end-1c"))

    tk.Button(credentials_window, text="Submit", command=on_submit).place(relx=0.5, rely=0.6, anchor='n')

    inputUser.place(relx=0.5, rely=0.1, anchor='n')
    inputP1.place(relx=0.5, rely=0.25, anchor='n')
    inputP2.place(relx=0.5, rely=0.4, anchor='n')

    credentials_window.mainloop()

def verify(user, pass1, pass2):
    verification_window = Toplevel()
    if pass1 == pass2 and len(pass1) >= 10 and has_numbers(pass1) and special_characters(pass1):
        update_userdata(user, pass1)
        Label(verification_window, text="Credentials added").pack()
    else:
        Label(verification_window, text="Password doesn't meet requirements").pack()

    verification_window.mainloop()

if __name__ == "__main__":
    first_window()
