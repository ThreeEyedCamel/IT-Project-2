#https://www.youtube.com/watch?v=MeMCBdnhvQs
import tkinter
import mazeEditorTkinter

credentials = [['user', 'pwd'],
               ['user2', 'pwd2']
]


#Create login function
def login():
    username = User_entry.get()
    password = Pwd_entry.get()
    valid = False
    for user, pwd in credentials:
        if user == username and pwd == password:
            valid = True
            print("Login success!!")
            break
        else:
            print("Login Failed")
    if valid == True:
        window.destroy()
        app = mazeEditorTkinter.MazeEditor()
        app.mainloop()

#Setup window
window = tkinter.Tk()
window.title("Login")
window.geometry('340x440')
#window.configure(bg='#333333')

#Creating components
login_Label = tkinter.Label(window, text = "Login")
User_Label = tkinter.Label(window, text = "Username: ")
User_entry = tkinter.Entry(window)
Pwd_Label = tkinter.Label(window, text = "Password: ")
Pwd_entry = tkinter.Entry(window, show = '*')
login_button = tkinter.Button(window, text = "Login", command=login)

#Placing components
login_Label.place(relx=0.5, rely=0, anchor='n')
User_Label.place(relx=0.5, rely=0.1, anchor='n')
User_entry.place(relx=0.5, rely=0.15, anchor='n')
Pwd_Label.place(relx=0.5, rely=0.25, anchor='n')
Pwd_entry.place(relx=0.5, rely=0.3, anchor='n')
login_button.place(relx=0.5, rely=0.4, anchor='n')

window.mainloop()
