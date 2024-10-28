import datetime
import re
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import DateEntry
from tkinter import messagebox as ms
from data import MySQL


class StudentManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Manager")
        self.root.resizable(0, 0)

        self.root.iconbitmap('img/icon_student.ico')

        self.db = MySQL()
        # menubar
        self.menubar = tk.Menu(self.root)

        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.root.quit)
        self.menubar.add_cascade(label='File', menu=self.file_menu)

        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label='Copy')
        self.edit_menu.add_command(label='Paste')
        self.menubar.add_cascade(label='Edit', menu=self.edit_menu)

        self.help_menu = tk.Menu(self.menubar, tearoff=0)
        self.help_menu.add_command(label='About')
        self.menubar.add_cascade(label='Help', menu=self.help_menu)

        self.root.config(menu=self.menubar)

        # Variables
        self.lf_bg = 'SteelBlue'
        self.labelfont = ('Calibri', 14)
        self.entryfont = ('Calibri', 14)

        self.name_strvar = tk.StringVar()
        self.email_strvar = tk.StringVar()
        self.contact_strvar = tk.StringVar()
        self.gender_strvar = tk.StringVar()
        self.stream_strvar = tk.StringVar()

        
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="STUDENT MANAGEMENT SYSTEM", font=self.labelfont, bg='SkyBlue').grid(row=0, columnspan=2, sticky='snew')
        self.frame_Left()
        self.frame_Rights()

    def frame_Left(self):
        self.left_frame = tk.Frame(self.root, bg=self.lf_bg)
        self.left_frame.grid(row=1, column=0, sticky='snew')

        # Labels
        tk.Label(self.left_frame, text="Name", font=self.labelfont, bg=self.lf_bg).grid(row=1, column=0, sticky='w', pady=(30, 0))
        tk.Label(self.left_frame, text="Contact Number", font=self.labelfont, bg=self.lf_bg).grid(row=2, column=0, sticky='w', pady=(10, 0))
        tk.Label(self.left_frame, text="Email Address", font=self.labelfont, bg=self.lf_bg).grid(row=3, column=0, sticky='w', pady=(10, 0))
        tk.Label(self.left_frame, text="Gender", font=self.labelfont, bg=self.lf_bg).grid(row=4, column=0, sticky='w', pady=(10, 0))
        tk.Label(self.left_frame, text="Date of Birth", font=self.labelfont, bg=self.lf_bg).grid(row=5, column=0, sticky='w', pady=(10, 0))
        tk.Label(self.left_frame, text="Stream", font=self.labelfont, bg=self.lf_bg).grid(row=6, column=0, sticky='w', pady=(10, 0))

        # Entry fields
        tk.Entry(self.left_frame, textvariable=self.name_strvar, font=self.entryfont).grid(row=1, column=1, sticky='e', pady=(25, 0), padx=(0, 20))
        tk.Entry(self.left_frame, textvariable=self.contact_strvar, font=self.entryfont).grid(row=2, column=1, sticky='e', pady=(10, 0), padx=(0, 20))
        tk.Entry(self.left_frame, textvariable=self.email_strvar, font=self.entryfont).grid(row=3, column=1, sticky='e', pady=(10, 0), padx=(0, 20))
        tk.Entry(self.left_frame, textvariable=self.stream_strvar, font=self.entryfont).grid(row=6, column=1, sticky='e', pady=(10, 0), padx=(0, 20))

        # Combobox
        self.gender_options = ['Male', 'Female', 'Other']
        ttk.Combobox(self.left_frame, textvariable=self.gender_strvar, values=self.gender_options, state='readonly', width=13).grid(row=4, column=1, sticky='w', pady=(10, 0))

        # DateEntry
        self.dob = DateEntry(self.left_frame, font=("Arial", 12), width=12)
        self.dob.grid(row=5, column=1, sticky='w', pady=(10, 0))

        tk.Button(self.left_frame, text='Submit', font=self.labelfont, width=13, command=self.add_record).grid(row=7, column=0, columnspan=2, pady=(30, 0))
        tk.Button(self.left_frame, text='Delete', font=self.labelfont, width=10, command=self.delete_record).grid(row=8, column=0, pady=(20, 0), sticky='e')
        tk.Button(self.left_frame, text='View', font=self.labelfont, width=10, command=self.view_records).grid(row=8, column=1, pady=(20, 0))
        tk.Button(self.left_frame, text='Clear', font=self.labelfont, width=10, command=self.reset_fields).grid(row=9, column=0, pady=10, sticky='e')
        tk.Button(self.left_frame, text='Update', font=self.labelfont, width=10, command=self.update_record).grid(row=9, column=1, padx=10, pady=10)

    def frame_Rights(self):
        self.right_frame = tk.Frame(self.root, bg="gray")
        self.right_frame.grid(row=1, column=1, sticky='snew')

        tk.Label(self.right_frame, text='Students Records', font='Arial', bg='DarkBlue', fg='LightCyan').grid(row=0, column=0, sticky='we', columnspan=2)

        # # Create Treeview
        self.tree = ttk.Treeview(self.right_frame, selectmode=tk.BROWSE, columns=('Stud ID', "Name", "Email Addr", "Contact No", "Gender", "Date of Birth", "Stream"))
        self.tree.grid(row=1, column=0, sticky='nsew')

        # # Create Scrollbars
        X_scroller = ttk.Scrollbar(self.right_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        Y_scroller = ttk.Scrollbar(self.right_frame, orient=tk.VERTICAL, command=self.tree.yview)

        self.tree.configure(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)

        self.tree.heading('Stud ID', text='ID', anchor=tk.CENTER)
        self.tree.heading('Name', text='Name', anchor=tk.CENTER)
        self.tree.heading('Email Addr', text='Email ID', anchor=tk.CENTER)
        self.tree.heading('Contact No', text='Phone No', anchor=tk.CENTER)
        self.tree.heading('Gender', text='Gender', anchor=tk.CENTER)
        self.tree.heading('Date of Birth', text='DOB', anchor=tk.CENTER)
        self.tree.heading('Stream', text='Stream', anchor=tk.CENTER)

        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('#1', width=30, stretch=tk.NO)
        self.tree.column('#2', width=120, stretch=tk.NO)
        self.tree.column('#3', width=180, stretch=tk.NO)
        self.tree.column('#4', width=90, stretch=tk.NO)
        self.tree.column('#5', width=60, stretch=tk.NO)
        self.tree.column('#6', width=80, stretch=tk.NO)
        self.tree.column('#7', width=120, stretch=tk.NO)

        X_scroller.grid(row=2, column=0, sticky='snew')
        Y_scroller.grid(row=1, column=1, sticky='ns')

        self.right_frame.grid_rowconfigure(1, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        # Bind double-click event to view record details
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])

        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    row = line.strip().split(',')
                    self.tree.insert('', 'end', values=row)
        except Exception as e:
            ms.showerror("Error", f"Failed to open file: {e}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv"), ("All files", "*.*")])

        if not file_path:
            return
        
        try:
            with open(file_path, 'w', encoding='utf-8') as txtfile:
                for row in self.tree.get_children():
                    values = self.tree.item(row)['values']
                    line = ','.join(map(str, values))  # Chuyển đổi giá trị thành chuỗi
                    txtfile.write(line + '\n')  # Ghi mỗi dòng vào tệp
            ms.showinfo("Success", "Data saved successfully!")
        except Exception as e:
            ms.showerror("Error", f"Failed to save file: {e}")

    def add_record(self):
        name = self.name_strvar.get()
        email = self.email_strvar.get()
        contact = self.contact_strvar.get()
        gender = self.gender_strvar.get()
        dob = self.dob.get_date()
        stream = self.stream_strvar.get()

        if not all([name, email, contact, gender, dob, stream]):
            ms.showerror("Error", "All fields are required!")
            return
        
        if not self.validation_email(email):
            ms.showerror("Error", "Invalid email address!")
            return

        try:
            self.db.insert_student(name, email, contact, gender, dob, stream)
            ms.showinfo("Success", "Record added to database!")
        except Exception as e:
            ms.showerror("Error", f"Failed to add record to database: {e}")

    def validation_email(self, email):
        pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
        return re.match(pattern, email) is not None
    
    def reset_fields(self):
        fields = [self.name_strvar, self.email_strvar, self.contact_strvar, self.gender_strvar, self.stream_strvar]
        for field in fields:
            field.set('')  # Clear the variable
        self.dob.set_date(datetime.datetime.now().date())

    def view_records(self):
        for record in self.tree.get_children():
            self.tree.delete(record)

        try:
            records = self.db.showStudent()
            for row in records:
                self.tree.insert('', 'end', values=row)
            if not records:
                ms.showinfo("Info", "No records found in the database!")
        except Exception as e:
            ms.showerror("Error", f"Failed to retrieve records from database: {e}")

    def update_record(self):
        selected_item = self.tree.selection()  # Get selected item
        if not selected_item:
            ms.showwarning("Warning", "Please select a record to update.")
            return
    
        student_id = self.tree.item(selected_item)['values'][0]  # Assuming ID is the first column
        name = self.name_strvar.get()
        email = self.email_strvar.get()
        contact = self.contact_strvar.get()
        gender = self.gender_strvar.get()
        dob = self.dob.get_date()
        stream = self.stream_strvar.get()

        if not all([name, email, contact, gender, dob, stream]):
            ms.showerror("Error", "All fields are required!")
            return

        if not self.validation_email(email):
            ms.showerror("Error", "Invalid email address!")
            return
        
        try:
            self.db.update_record(student_id, name, email, contact, gender, dob, stream)
            ms.showinfo("Success", "Record updated successfully!")
            self.view_records()  # Refresh the view after update
        except Exception as e:
            ms.showerror("Error", f"Failed to update record: {e}")

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            ms.showwarning("Warning", "Please select a record to delete.")
            return

        student_id = self.tree.item(selected_item)['values'][0]
        print(student_id)

        confirm = ms.askyesno("Confirm Delete", "Are you sure you want to delete this record?")
        if confirm:
            try:
                self.db.delete_record(student_id)
                self.tree.delete(selected_item)
                ms.showinfo("Success", "Record deleted successfully!")
            except Exception as e:
                ms.showerror("Error", f"Failed to delete record: {e}")

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item)
            student_id, name, email, contact, gender, dob, stream = item['values']
        
            self.name_strvar.set(name)
            self.email_strvar.set(email)
            self.contact_strvar.set(contact)
            self.gender_strvar.set(gender)
        
            # Nếu dob là chuỗi, bạn cần chuyển đổi nó thành datetime.date
            if isinstance(dob, str):
                dob = datetime.datetime.strptime(dob, "%Y-%m-%d").date()
        
            self.dob.set_date(dob)  # Đặt ngày sinh
            self.stream_strvar.set(stream)


if __name__ == '__main__':
    root = tk.Tk()
    app = StudentManager(root)
    root.mainloop()
