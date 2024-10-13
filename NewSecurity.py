#https://www.youtube.com/watch?v=MeMCBdnhvQs
import tkinter
import mazeEditorTkinter

credentials = [['user', 'pwd'],
               ['user2', 'pwd2']
]


#Create login function
def login(username, password):
    print(username, password)
    valid = False
    for user, pwd in credentials:
        if user == username and pwd == password:
            valid = True
            print("Login success!!")
            break
        else:
            print("Login Failed")
    if valid == True:
        main_window.destroy()
        app = mazeEditorTkinter.MazeEditor()
        app.mainloop()

def set_credentials(username, password):
    credentials.append([username, password])

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
    #Placing components
    login_Label2.place(relx=0.5, rely=0, anchor='n')
    User_Label2.place(relx=0.5, rely=0.1, anchor='n')
    User_entry2.place(relx=0.5, rely=0.15, anchor='n')
    Pwd_Label2.place(relx=0.5, rely=0.25, anchor='n')
    Pwd_entry2.place(relx=0.5, rely=0.3, anchor='n')
    set_button2.place(relx=0.5, rely=0.4, anchor='n')
    login_button2.place(relx=0.5, rely=0.45, anchor='n')



login_button_main = tkinter.Button(main_window, text = "Login", command=login_window)
Set_button_main = tkinter.Button(main_window, text = "Set Credentials", command=credential_window)
login_button_main.place(relx=0.5, rely=0.4, anchor='n')
Set_button_main.place(relx=0.5, rely=0.5, anchor='n')

main_window.mainloop()