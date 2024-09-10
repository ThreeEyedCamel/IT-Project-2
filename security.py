# Author Nicky
# Last update: 02/09/2024
"""
INTEGRATION NOTE:
connection_result is where to call the GUI - its commented 
"""
import sqlite3
import hashlib
import sqlite3
import hashlib
import socket
import threading
import re
from tkinter import *
import tkinter as tk

#Setting up the userdata database
def security_setup():
    #Connect to database - need to create the database
    conn = sqlite3.connect("userdata.db")
    #Cursor for the connection
    cur = conn.cursor()

    #Create the table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY,         
                username VARCHAR(255) NOT NULL, 
                password VARCHAR(255) NOT NULL
                )
    """)

    #Setup some data to test, ensuring the username is encoded
    username1, password1 = 'User1', hashlib.sha256("password1".encode()).hexdigest() 
    username2, password2 = 'User2', hashlib.sha256("password2".encode()).hexdigest() 
    username3, password3 = 'User3', hashlib.sha256("password3".encode()).hexdigest() 
    username4, password4 = 'User4', hashlib.sha256("password4".encode()).hexdigest() 
    username5, password5 = 'User5', hashlib.sha256("password5".encode()).hexdigest()

    #Place this data into the table
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)",(username1, password1)) 
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)",(username2, password2)) 
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)",(username3, password3)) 
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)",(username4, password4)) 
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)",(username5, password5)) 
    conn.commit()

    #Print out DB contents
    cur.execute("SELECT * FROM userdata")
    result = cur.fetchall()
    print(result)
    conn.close()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

#Update the database with new credentials
def update_userdata(username, password):
    conn = sqlite3.connect("userdata.db")
    #Cursor for the connection
    cur = conn.cursor()

    #Create the table if it doesnt exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
                id INTEGER PRIMARY KEY,         
                username VARCHAR(255) NOT NULL, 
                password VARCHAR(255) NOT NULL
                )
    """)

    #update the table with the newest data
    username1, password1 = username, hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO userdata(username, password) VALUES(?,?)",(username1, password1))
    conn.commit()
    print("Database updated!")
    conn.close()

#Login to the app
#Password is being sent in cleartext
def handle_connection(c):

    try: 
        root4 = Tk()
        root4.title("Set Credentials")
        root4.geometry("500x500+50+50")  # width x height + x + y

        #Make labels
        text = Label(root4, text="Login")
        textU = Label(root4, text="Username:")
        textP1 = Label(root4, text="Password:")
        #Define input boxes
        inputUser = tk.Text(root4, 
                    height = 2, 
                    width = 20) 
        inputP1 = tk.Text(root4, 
                    height = 2, 
                    width = 20) 
        username, password = inputUser.get(1.0, "end-1c"), inputP1.get(1.0, "end-1c")
        #Define button
        submitButton = tk.Button(root4, 
                            text = "Submit",  
                            command = lambda: connection_result(c,inputUser.get(1.0, "end-1c"), inputP1.get(1.0, "end-1c"))
                            ) 
        text.pack()
        textU.place(relx=0.5, rely=0.05, anchor='n')
        textP1.place(relx=0.5, rely=0.2, anchor='n')

        inputUser.place(relx=0.5, rely=0.1, anchor='n')
        inputP1.place(relx=0.5, rely=0.25, anchor='n')

        #Place buttons
        submitButton.place(relx=0.5, rely=0.6, anchor='n')
        
        
        root4.mainloop()
    finally:
        c.close()


def connection_result(c,username, password):
        
        password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(r"C:\Users\domin\Desktop\IT Project 2\userdata.db")
        cur = conn.cursor()
        
        #Preset the statement to help avoid sql injection
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
        
        if cur.fetchall(): #If it returns true its correct password
            root5 = Tk()
            text1 = Label(root5, text="Login successful!")
            text1.pack()
            c.send("Login successful!".encode())
            #Call the GUI function
        else:
            root5 = Tk()
            text1 = Label(root5, text="Login FAILED")
            text1.pack()
            c.send("Login FAILED".encode())
        

def client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("localhost", 9999)) 

    message = client.recv(1024).decode()
    client.send(input(message).encode())

    message = client.recv(1024).decode()
    client.send(input(message).encode()) 

    #Print if it was successful or not
    print(client.recv(1024).decode())

#Main loop to accept connections
def start_server():
    print("Server is listening...")
    while True:
        client, addr = server.accept()
        threading.Thread(target=handle_connection, args=(client,)).start()


def main():
    #The server and client need to be called in seperate threads as they must occur at the same time 
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True  #Server will close when main program closes
    server_thread.start()
    #Client will start in the main thread
    client()


def has_numbers(string):
    return bool(re.search(r'\d', string))


def special_characters(string):
    characters = "!@#$%^&*()-+?_=,<>/"
    if any(i in characters for i in string):
        result = True
    else:
        result = False
    return result


def first_window():
    root1 = Tk()
    root1.title("Choice")
    
    setButton = tk.Button(root1, 
                        text = "Set credentials",  
                        command = set_credentials
                        ) 
    loginButton = tk.Button(root1, 
                        text = "Login",  
                        command = main
                        ) 
    setButton.place(relx=0.5, rely=0.2, anchor='n')
    loginButton.place(relx=0.5, rely=0.4, anchor='n')
    

    root1.mainloop()


def set_credentials():
    root = Tk()
    root.title("Set Credentials")
    root.geometry("500x500+50+50")  # width x height + x + y

    #Make labels
    text = Label(root, text="Login")
    textU = Label(root, text="Username:")
    textP1 = Label(root, text="Password:")
    textP2 = Label(root, text="Re-enter password: ")
    req = Label(root, text="Password requirements:\n 10 characters long \n Contains numbers \n Contains a special character")

    #Define input boxes
    inputUser = tk.Text(root, 
                   height = 2, 
                   width = 20) 
    inputP1 = tk.Text(root, 
                   height = 2, 
                   width = 20) 
    inputP2 = tk.Text(root, 
                   height = 2, 
                   width = 20)  
    
    
    #Define button
    submitButton = tk.Button(root, 
                        text = "Submit",  
                        command = lambda: verify(inputUser.get(1.0, "end-1c"), inputP1.get(1.0, "end-1c"), inputP2.get(1.0, "end-1c"))
                        ) 

    text.pack()

    #Place labels
    textU.place(relx=0.5, rely=0.05, anchor='n')
    textP1.place(relx=0.5, rely=0.2, anchor='n')
    textP2.place(relx=0.5, rely=0.35, anchor='n')
    req.place(relx=0.5, rely=0.8, anchor='n')
    #Place buttons
    submitButton.place(relx=0.5, rely=0.6, anchor='n')
    #Place input boxes
    inputUser.place(relx=0.5, rely=0.1, anchor='n')
    inputP1.place(relx=0.5, rely=0.25, anchor='n')
    inputP2.place(relx=0.5, rely=0.4, anchor='n')

    root.mainloop()
    

def verify(user, pass1, pass2):
    match = False
    root3 = Tk()
    
    if pass1 == pass2 and len(pass1) >=10 and has_numbers(pass1) == True and special_characters(pass1) == True:
            match = True
            update_userdata(user, pass1)
            text1 = Label(root3, text="Credentials added")
            text1.pack()
            
    else:
            text2 = Label(root3, text="Password doesn't meet requirements")
            text2.pack()
            match = False

    root3.mainloop()
    return match


if __name__ == "__main__":
    first_window()