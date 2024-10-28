import tkinter as tk
from data import MySQL
from tkinter import messagebox as ms
import customtkinter as ctk

from view_student import StudentManager

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.configure(bg='#fff')
        self.root.resizable(0, 0)

        self.root.iconbitmap('img/icon_student.ico')

        self.etr_user = tk.StringVar()
        self.entr_pass = tk.StringVar()

        self.db = MySQL()

        self.img = tk.PhotoImage(file='img/login.png')

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, image=self.img, bg='white').grid(row=0, column=0, sticky='snew')

        self.frame = tk.Frame(self.root, width=350, height=350, bg='white')
        self.frame.grid(row=0, column=1)

        self.heading = tk.Label(self.frame, text='Sign in', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
        self.heading.grid(row=0, column=0, columnspan=2, sticky='ew')

        # Tạo trường nhập cho Username
        self.user_entry_frame = tk.Frame(self.frame, bg='white')
        self.user_entry_frame.grid(row=1, column=0, sticky='ew')

        self.user_entry = tk.Entry(self.user_entry_frame, textvariable=self.etr_user, width=25, fg='black', border=0, bg='white',
                                   font=('Microsoft Yahei UI Light', 11))
        self.user_entry.grid(row=0, column=0, pady=(10, 0))
        self.user_entry.insert(0, "Username")
        self.user_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(self.user_entry, "Username"))
        self.user_entry.bind('<FocusOut>', lambda e: self.set_placeholder(self.user_entry, "Username"))

        self.user_underline = tk.Frame(self.user_entry_frame, bg='black', height=2)
        self.user_underline.grid(row=1, column=0, sticky='ew', pady=(0, 10))

        # Tạo trường nhập cho Password
        self.password_entry_frame = tk.Frame(self.frame, bg='white')
        self.password_entry_frame.grid(row=2, column=0, sticky='ew')

        self.password_entry = tk.Entry(self.password_entry_frame, textvariable=self.entr_pass, width=25, fg='black', border=0, bg='white',
                                       font=('Microsoft Yahei UI Light', 11), show='*')
        self.password_entry.grid(row=0, column=0, pady=(10, 0))
        self.password_entry.insert(0, "Password")
        self.password_entry.bind('<FocusIn>', lambda e: self.clear_placeholder(self.password_entry, "Password"))
        self.password_entry.bind('<FocusOut>', lambda e: self.set_placeholder(self.password_entry, "Password"))

        self.password_underline = tk.Frame(self.password_entry_frame, bg='black', height=2)
        self.password_underline.grid(row=1, column=0, sticky='ew', pady=(0, 10))

        # Button Login
        ctk.CTkButton(self.frame, width=80, height=30, text='Sign in', text_color='white', corner_radius=5,command=self.login_user).grid(row=3, columnspan=2, pady=(10, 0))
        lbl_forgot = tk.Label(self.frame, text="Don't have an account", fg='black', bg='white', cursor='hand2', font=('Microsoft Yahei UI Light', 10))
        lbl_forgot.grid(row=4, column=0, sticky='w')

        self.sign_up = tk.Button(self.frame, text="Sign up", fg='white', border=0, bg='white', cursor='hand2', foreground='#57a1f8', font=('Microsoft Yahei UI Light', 10))
        self.sign_up.grid(row=4, column=0, pady=15, sticky='e')

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def set_placeholder(self, entry, placeholder):
        if entry.get() == '':
            entry.insert(0, placeholder)

    def login_user(self):
        username = self.etr_user.get()
        password = self.entr_pass.get()

        if username == '' or password == '':
            ms.showerror("Error", "Please fill in all fields!")
            return
    
        if self.db.login(username, password):
            ms.showinfo("Success", "Login successful!")
            self.root.destroy()
            
            main_window = tk.Tk()
            StudentManager(main_window)
            main_window.mainloop()
        else:
            ms.showerror("Error", "Invalid username or password!")
            
if __name__ == '__main__':
    root = tk.Tk()
    login_gui = Login(root)
    root.mainloop()
