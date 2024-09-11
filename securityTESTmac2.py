import sqlite3
import hashlib
import socket
import threading
import re
from tkinter import *
import tkinter as tk
from tkinter import messagebox

# Database setup
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
    # Run Tkinter GUI in the main thread
    def show_credentials_window():
        def on_submit():
            username = inputUser.get(1.0, "end-1c")
            password = inputP1.get(1.0, "end-1c")
            connection_result(username, password)
            root4.destroy()

        root4 = tk.Tk()
        root4.title("Set Credentials")
        root4.geometry("500x500+50+50")

        tk.Label(root4, text="Login").pack()
        tk.Label(root4, text="Username:").place(relx=0.5, rely=0.05, anchor='n')
        tk.Label(root4, text="Password:").place(relx=0.5, rely=0.2, anchor='n')

        inputUser = tk.Text(root4, height=2, width=20)
        inputP1 = tk.Text(root4, height=2, width=20)

        inputUser.place(relx=0.5, rely=0.1, anchor='n')
        inputP1.place(relx=0.5, rely=0.25, anchor='n')

        submitButton = tk.Button(root4, text="Submit", command=on_submit)
        submitButton.place(relx=0.5, rely=0.6, anchor='n')

        root4.mainloop()

    show_credentials_window()

def connection_result(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    conn = sqlite3.connect("userdata.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
    result = cur.fetchall()
    conn.close()
    
    msg = "Login successful!" if result else "Login FAILED"
    
    # Update GUI on the main thread
    def show_result_window():
        root5 = tk.Tk()
        tk.Label(root5, text=msg).pack()
        root5.mainloop()

    # Display result in the main thread
    show_result_window()
    c.send(msg.encode())

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
    def on_set_credentials():
        # Create a new thread for the GUI so it does not block the main thread
        threading.Thread(target=set_credentials).start()

    root1 = tk.Tk()
    root1.title("Choice")

    tk.Button(root1, text="Set credentials", command=on_set_credentials).place(relx=0.5, rely=0.2, anchor='n')
    tk.Button(root1, text="Login", command=main).place(relx=0.5, rely=0.4, anchor='n')

    root1.mainloop()

def set_credentials():
    def on_submit():
        verify(inputUser.get(1.0, "end-1c"), inputP1.get(1.0, "end-1c"), inputP2.get(1.0, "end-1c"))

    root = tk.Tk()
    root.title("Set Credentials")
    root.geometry("500x500+50+50")

    tk.Label(root, text="Login").pack()
    tk.Label(root, text="Username:").place(relx=0.5, rely=0.05, anchor='n')
    tk.Label(root, text="Password:").place(relx=0.5, rely=0.2, anchor='n')
    tk.Label(root, text="Re-enter password: ").place(relx=0.5, rely=0.35, anchor='n')
    tk.Label(root, text="Password requirements:\n 10 characters long \n Contains numbers \n Contains a special character").place(relx=0.5, rely=0.8, anchor='n')

    inputUser = tk.Text(root, height=2, width=20)
    inputP1 = tk.Text(root, height=2, width=20)
    inputP2 = tk.Text(root, height=2, width=20)

    tk.Button(root, text="Submit", command=on_submit).place(relx=0.5, rely=0.6, anchor='n')

    inputUser.place(relx=0.5, rely=0.1, anchor='n')
    inputP1.place(relx=0.5, rely=0.25, anchor='n')
    inputP2.place(relx=0.5, rely=0.4, anchor='n')

    root.mainloop()

def verify(user, pass1, pass2):
    if pass1 == pass2 and len(pass1) >= 10 and has_numbers(pass1) and special_characters(pass1):
        update_userdata(user, pass1)
        messagebox.showinfo("Success", "Credentials added")
    else:
        messagebox.showwarning("Failure", "Password doesn't meet requirements")

if __name__ == "__main__":
    first_window()
