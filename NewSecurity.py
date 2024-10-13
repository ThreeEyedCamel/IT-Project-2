#https://www.youtube.com/watch?v=MeMCBdnhvQs
import re
import tkinter
from tkinter import messagebox
import mazeEditorTkinter

credentials = [['user', 'pass12345678910!'],
               ['user2', 'pass12345678910!']
]

def has_numbers(string):
    return bool(re.search(r'\d', string))


def special_characters(string):
    characters = "!@#$%^&*()-+?_=,<>/"
    if any(i in characters for i in string):
        result = True
    else:
        result = False
    return result


#Create login function
def login(username, password):
    valid = False
    for user, pwd in credentials:
        if user == username and pwd == password:
            valid = True
            break
        else:
            valid == False
            
    if valid == True:
        messagebox.showinfo(title="Login Success", message="Login successful!")
        print("Login success!!")
        main_window.destroy()
        app = mazeEditorTkinter.MazeEditor()
        app.mainloop()
    else:
        print("Login Failed")
        messagebox.showinfo(title="Login Failed", message="Login Failed, please try again")



def set_credentials(username, password):
    if len(password) >=14 and special_characters(password) == True and  has_numbers(password) == True:
        credentials.append([username, password])
        messagebox.showinfo(title="Credentials added", message="Credentials added, please log in")
    else:
        messagebox.showinfo(title="Password doesn't meet requirements", message="Password doesn't meet requirements. \n Please try again")

#Setup main window
main_window = tkinter.Tk()
main_window.title("Login")
main_window.geometry('340x440')

def login_window():
    window = tkinter.Toplevel(main_window)
    window.title("Login")
    window.geometry('340x440')

    #Creating components
    login_Label = tkinter.Label(window, text = "Login")
    User_Label = tkinter.Label(window, text = "Username: ")
    User_entry = tkinter.Entry(window)
    Pwd_Label = tkinter.Label(window, text = "Password: ")
    Pwd_entry = tkinter.Entry(window, show = '*')
    

   

    login_button = tkinter.Button(window, text = "Login", command=lambda: login(User_entry.get(), Pwd_entry.get()))

    #Placing components
    login_Label.place(relx=0.5, rely=0, anchor='n')
    User_Label.place(relx=0.5, rely=0.1, anchor='n')
    User_entry.place(relx=0.5, rely=0.15, anchor='n')
    Pwd_Label.place(relx=0.5, rely=0.25, anchor='n')
    Pwd_entry.place(relx=0.5, rely=0.3, anchor='n')
    login_button.place(relx=0.5, rely=0.4, anchor='n')
    



def credential_window():
    #Setup window for set pwd screen
    window2 = tkinter.Toplevel(main_window)
    window2.title("Set Credentials")
    window2.geometry('340x440')
    #Creating components
    login_Label2 = tkinter.Label(window2, text = "Set Credentials")
    User_Label2 = tkinter.Label(window2, text = "Username: ")
    User_entry2 = tkinter.Entry(window2)
    Pwd_Label2 = tkinter.Label(window2, text = "Password: ")
    Pwd_entry2 = tkinter.Entry(window2, show = '*')
    set_button2 = tkinter.Button(window2, text = "Set", command=lambda: set_credentials(User_entry2.get(), Pwd_entry2.get()))
    login_button2 = tkinter.Button(window2, text = "Login", command=login_window)
    requirements_Label = tkinter.Label(window2, text = "Password must be at least 14 characters \n contain a number and a special character")


    #Placing components
    login_Label2.place(relx=0.5, rely=0, anchor='n')
    User_Label2.place(relx=0.5, rely=0.1, anchor='n')
    User_entry2.place(relx=0.5, rely=0.15, anchor='n')
    Pwd_Label2.place(relx=0.5, rely=0.25, anchor='n')
    Pwd_entry2.place(relx=0.5, rely=0.3, anchor='n')
    set_button2.place(relx=0.5, rely=0.4, anchor='n')
    login_button2.place(relx=0.5, rely=0.45, anchor='n')
    requirements_Label.place(relx=0.5, rely=0.5, anchor='n')



login_button_main = tkinter.Button(main_window, text = "Login", command=login_window)
Set_button_main = tkinter.Button(main_window, text = "Set Credentials", command=credential_window)
login_button_main.place(relx=0.5, rely=0.4, anchor='n')
Set_button_main.place(relx=0.5, rely=0.5, anchor='n')

main_window.mainloop()