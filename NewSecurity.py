import re
import tkinter
from tkinter import messagebox
import mazeEditorTkinter
import hashlib
"""
This function is the security function. 
"""
#Basic database to start with
credentials = [['user', 'Password12345!'],
               ['user2', 'Password67890!']
]

#Function to hash/encrypt the passwords:
def hash_pass(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Function to check if the password has numbers (returns bool true/false)
def has_numbers(string):
    return bool(re.search(r'\d', string))

#Function to check if the password has special characters  (returns bool true/false)
def special_characters(string):
    characters = "!@#$%^&*()-+?_=,<>/"
    if any(i in characters for i in string):
        result = True
    else:
        result = False
    return result


#Create login function
def login(username, password):
    hashed_password1 = password
    valid = False
    #Check if the provided username and password are valid or not
    for user, pwd in credentials:
        if user == username and pwd == hashed_password1:
            valid = True
            break
        else:
            valid == False

    #If the credentials are valid close the windows and log in    
    if valid == True:
        messagebox.showinfo(title="Login Success", message="Login successful!")
        print("Login success!!")
        main_window.destroy()
        app = mazeEditorTkinter.MazeEditor()
        app.mainloop()
    #If the credentials are not valid throw an error
    else:
        print("Login Failed")
        messagebox.showinfo(title="Login Failed", message="Login Failed, please try again")


#Function to set the users credentials
def set_credentials(username, password1, password2):
    #Check the username is valid and not taken
    if len(username) > 0 and not any(username in sublist for sublist in credentials):
        #Check the password has been correctly inputted twice
        if password1 == password2:
            #Check the password meets requirements
            if len(password1) >=14 and special_characters(password1) == True and  has_numbers(password1) == True:
                hashed_password = hash_pass(password1)
                #Add the credentials to the database and inform the user of the success
                credentials.append([username, hashed_password])
                messagebox.showinfo(title="Credentials added", message="Credentials added, please log in")
            #Inform the user they didn't enter a valid password
            else:
                messagebox.showinfo(title="Password doesn't meet requirements", message="Password doesn't meet requirements. \n Please try again")
        #Inform the user their passwords entered don't match
        else:
            messagebox.showinfo(title="Passwords don't match", message="Passwords don't match. \n Please try again")
    #Inform the user their username is invalid or taken
    else:
        messagebox.showinfo(title="Username error", message="Username is either invalid or taken. \n Please try again")

#Setup main window - all other windows are toplevels of this window
main_window = tkinter.Tk()
main_window.title("Login")
main_window.geometry('340x440')

#Define the login window to access the app
def login_window():
    #Create a new toplevel window for the login screen
    window = tkinter.Toplevel(main_window)
    window.title("Login")
    window.geometry('340x440')

    #Creating components
    login_Label = tkinter.Label(window, text = "Login")             #Title
    User_Label = tkinter.Label(window, text = "Username: ")         #Username label
    User_entry = tkinter.Entry(window)                              #Username input box
    Pwd_Label = tkinter.Label(window, text = "Password: ")          #Password label
    Pwd_entry = tkinter.Entry(window, show = '*')                   #Password input box - * added for privacy
    login_button = tkinter.Button(window, text = "Login", background='light blue', command=lambda: login(User_entry.get(), Pwd_entry.get())) #Button to verify login details

    #Placing components on the window
    login_Label.place(relx=0.5, rely=0, anchor='n')
    User_Label.place(relx=0.5, rely=0.1, anchor='n')
    User_entry.place(relx=0.5, rely=0.15, anchor='n')
    Pwd_Label.place(relx=0.5, rely=0.25, anchor='n')
    Pwd_entry.place(relx=0.5, rely=0.3, anchor='n')
    login_button.place(relx=0.5, rely=0.4, anchor='n')
    


#Define the credential window for the user to setup their username and password
def credential_window():
    #Make a new toplevel window for credential screen
    window2 = tkinter.Toplevel(main_window)
    window2.title("Set Credentials")
    window2.geometry('340x440')


    #Creating components
    login_Label2 = tkinter.Label(window2, text = "Set Credentials")         #Title
    User_Label2 = tkinter.Label(window2, text = "Username: ")               #Username label
    User_entry2 = tkinter.Entry(window2)                                    #Username input box
    Pwd_Label1 = tkinter.Label(window2, text = "Password: ")                #Password label
    Pwd_Label2 = tkinter.Label(window2, text = "Re-enter password: ")       #Re-enter Password label
    Pwd_entry1 = tkinter.Entry(window2, show = '*')                         #Password input box - * added for privacy
    Pwd_entry2 = tkinter.Entry(window2, show = '*')                         #Second password input box - * added for privacy
    set_button2 = tkinter.Button(window2, text = "Set", background='light blue',command=lambda: set_credentials(User_entry2.get(), Pwd_entry1.get(), Pwd_entry2.get())) #Button to set the credentials
    login_button2 = tkinter.Button(window2, text = "Login", background='light grey', command=login_window)   #Button to login after setting credentials
    requirements_Label = tkinter.Label(window2, text = "Password must be at least 14 characters \n contain a number and a special character") #Requirements label


    #Placing components
    login_Label2.place(relx=0.5, rely=0, anchor='n')
    User_Label2.place(relx=0.5, rely=0.1, anchor='n')
    User_entry2.place(relx=0.5, rely=0.15, anchor='n')
    Pwd_Label1.place(relx=0.5, rely=0.2, anchor='n')
    Pwd_entry1.place(relx=0.5, rely=0.25, anchor='n')
    Pwd_Label2.place(relx=0.5, rely=0.3, anchor='n')
    Pwd_entry2.place(relx=0.5, rely=0.35, anchor='n')
    set_button2.place(relx=0.5, rely=0.4, anchor='n')
    login_button2.place(relx=0.5, rely=0.47, anchor='n')
    requirements_Label.place(relx=0.5, rely=0.53, anchor='n')


#Main window 
#Define components
Welcome_Label = tkinter.Label(main_window, font = ("Comic Sans ms", 15), text = "Welcome to Trailblazer")                          #Welcome label
sub_welcome_label = tkinter.Label(main_window, font = ("Comic Sans ms", 10), text = "A Robotic Path Planning GUI!")                #App name label
informative_label = tkinter.Label(main_window,  font = ("Comic Sans ms", 8), text = "Please login or setup an account to start." ) #Instructional label
exist_user_label = tkinter.Label(main_window, font = ("Comic Sans ms", 13), text = "Existing Users: " )                            #Existing Users label
new_user_label = tkinter.Label(main_window, font = ("Comic Sans ms", 13),text = "New Users: " )                                    #New Users label
login_button_main = tkinter.Button(main_window, text = "Login", background='light blue', command=login_window)                     #Login button
Set_button_main = tkinter.Button(main_window, text = "Set Credentials", background='light blue', command=credential_window)        #Set credentials button

#Place components
exist_user_label.place(relx=0.5, rely=0.33, anchor='n')
login_button_main.place(relx=0.5, rely=0.4, anchor='n')
new_user_label.place(relx=0.5, rely=0.5, anchor='n')
Set_button_main.place(relx=0.5, rely=0.57, anchor='n')
Welcome_Label.place(relx=0.5, rely=0.075, anchor='n')
sub_welcome_label.place(relx=0.5, rely=0.15, anchor='n')
informative_label.place(relx=0.5, rely=0.25, anchor='n')


#Call the main window to start the program
main_window.mainloop()