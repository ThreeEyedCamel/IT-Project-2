import sqlite3
import hashlib
import sqlite3
import hashlib
import socket
import threading
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
    username1, password1 = 'Nicky1', hashlib.sha256("nickyspassword1".encode()).hexdigest() 
    username2, password2 = 'Nicky2', hashlib.sha256("nickyspassword2".encode()).hexdigest() 
    username3, password3 = 'Nicky3', hashlib.sha256("nickyspassword3".encode()).hexdigest() 
    username4, password4 = 'Nicky4', hashlib.sha256("nickyspassword4".encode()).hexdigest() 
    username5, password5 = 'Nicky5', hashlib.sha256("nickyspassword5".encode()).hexdigest()
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

#password is being sent in cleartext
def handle_connection(c):

    try: 
        c.send("Username: ".encode())
        username = c.recv(1024).decode()

        c.send("Password: ".encode())
        password = c.recv(1024).decode()
        password = hashlib.sha256(password.encode()).hexdigest()

        conn = sqlite3.connect(r"C:\Users\domin\Desktop\IT Project 2\userdata.db")
        cur = conn.cursor()
        
        #Preset the statement to help avoid sql injection
        cur.execute("SELECT * FROM userdata WHERE username = ? AND password = ?", (username, password))
        if cur.fetchall(): #If it returns true its correct password
            c.send("Login successful!".encode())
            #Call the GUI function
        else:
            c.send("Login FAILED".encode())
    finally:
        print("hello there")
        c.close()
        client()


def client():
    print("hi")
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

if __name__ == "__main__":
    main()