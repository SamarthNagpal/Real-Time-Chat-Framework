import socket
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import threading
import pickle


host = ''
port = 9998


class Program(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        window = Frame(self)
        window.pack(side="top", fill="both", expand=True)

        self.pages_list = [MenuPage, CreateProfilePage, EmailVerificationPage, LoginPage, SearchPage, SearchResults, ChatListWindow, ChatWindow]
        self.frames_dict = {}
        for F in self.pages_list:
            frame = F(window, self)
            self.frames_dict[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(SearchResults)

    def show_frame(self, cont):
        frame = self.frames_dict[cont]
        frame.tkraise()


class MenuPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        ttk.Button(self, text='Create A New Profile', command=lambda: controller.show_frame(CreateProfilePage)).pack(pady=5, fill='x')
        ttk.Button(self, text='Login To Existing Profile', command=lambda: controller.show_frame(LoginPage)).pack(pady=5, fill='x')
        ttk.Button(self, text='Search For A User', command=lambda: controller.show_frame(SearchPage)).pack(pady=5, fill='x')
        ttk.Button(self, text='Exit', command=exit).pack(pady=5, fill='x')


class CreateProfilePage(Frame):

    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent)
        n = 10
        Label(self, text='First Name').grid(row=0, column=0, sticky='e', pady=5)
        firstname_entry = Entry(self)
        firstname_entry.grid(row=0, column=1, pady=5)
        Label(self, text='Last Name').grid(row=1, column=0, sticky='e', pady=5)
        lastname_entry = Entry(self)
        lastname_entry.grid(row=1, column=1, pady=5)
        Label(self, text='Email Address').grid(row=2, column=0, sticky='e', pady=5)
        email_entry = Entry(self)
        email_entry.grid(row=2, column=1, pady=5)
        Label(self, text='Username').grid(row=3, column=0, sticky='e', pady=5)
        username_entry = Entry(self)
        username_entry.grid(row=3, column=1, pady=5)
        Label(self, text='Password').grid(row=4, column=0, sticky='e', pady=5)
        password_entry = Entry(self, show='*')
        password_entry.grid(row=4, column=1, pady=5)
        Label(self, text='Gender').grid(row=5, column=0, sticky='ne', pady=5, rowspan=3)
        self.gender = StringVar()
        Radiobutton(self, text='Male', variable=self.gender, value='Male').grid(row=5, column=1, pady=5, sticky='w')
        Radiobutton(self, text='Female', variable=self.gender, value='Female').grid(row=n - 4, column=1, pady=5, sticky='w')
        Radiobutton(self, text='Other', variable=self.gender, value='Other').grid(row=n - 3, column=1, pady=5, sticky='w')
        Label(self, text='Date Of Birth').grid(row=n - 2, column=0, sticky='e', pady=5)
        dob_entry = Entry(self, text='dd/mm/yyyy')
        dob_entry.grid(row=n - 2, column=1, pady=5)
        dob_entry.insert(0, 'DD/MM/YYYY')
        Checkbutton(self, text='Keep me logged in').grid(row=n - 1, column=0, columnspan=2, pady=5)
        ttk.Button(self, text='Go Back', command=lambda: self.controller.show_frame(MenuPage)).grid(row=n, column=0, pady=5)
        ttk.Button(self, text='Register', command=lambda: self.validity_check()).grid(row=n, column=1, pady=5)
        self.first_name, self.last_name, self.email, self.username, self.password, self.dob = firstname_entry.get(), lastname_entry.get(), email_entry.get(), username_entry.get(), password_entry.get(), dob_entry.get()

    def validity_check(self):
        error_title = 'Error!'
        print(self.username)
        if (bool(self.first_name) and bool(self.last_name) and bool(self.email) and bool(self.username) and bool(self.password) and bool(self.gender) and bool(self.dob)) is False:
            error_message = 'Empty Field!'
            self.controller.show_frame(CreateProfilePage)
            tkinter.messagebox.showinfo(error_title, error_message)
        elif self.email.count('@') != 1:
            error_message = 'Sorry, Invalid Email Id!'
            self.controller.show_frame(CreateProfilePage)
            tkinter.messagebox.showinfo(error_title, error_message)
        elif '.' not in self.email:
            error_message = 'Sorry, Invalid Email Id!'
            self.controller.show_frame(CreateProfilePage)
            tkinter.messagebox.showinfo(error_title, error_message)
        elif '.' in self.email and not self.email.split('.')[-1].isalpha():
            error_message = 'Sorry, Invalid Email Id!'
            self.controller.show_frame(CreateProfilePage)
            tkinter.messagebox.showinfo(error_title, error_message)
        elif self.dob.count('/') != 2:
            error_message = 'Sorry, Invalid Date Of Birth!'
            self.controller.show_frame(CreateProfilePage)
            tkinter.messagebox.showinfo(error_title, error_message)
        elif not self.dob.split('/')[0].isdigit() or len(self.dob.split('/')[0]) != 2 or not self.dob.split('/')[1].isdigit() or len(self.dob.split('/')[1]) != 2 or not self.dob.split('/')[2].isdigit() or len(self.dob.split('/')[2]) != 4:
            error_message = 'Sorry, Invalid Date Of Birth!'
            self.controller.show_frame(CreateProfilePage)
            tkinter.messagebox.showinfo(error_title, error_message)
        else:
            data_tuple = (self.first_name.capitalize(), self.last_name.capitalize(), self.email, self.username, self.password, self.gender, self.dob)
            data_dict = {'request': 'register', 'data': data_tuple}
            send_data(data_dict)
            self.controller.show_frame(EmailVerificationPage)


class EmailVerificationPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        verification_code = Entry(self)
        verification_code.grid(row=1, column=0, pady=5)
        ttk.Button(self, text='Verify', command=lambda: send_data(data_dict1)).grid(row=1, column=1, pady=5)
        ttk.Button(self, text='Go Back', command=lambda: controller.show_frame(CreateProfilePage)).grid(row=2, column=0, pady=5)
        ttk.Button(self, text='Resend Code', command=lambda: send_data(data_dict2)).grid(row=2, column=1, pady=5)
        data_dict1 = {'request': 'verification', 'code': verification_code.get()}
        data_dict2 = {'request': 'resend'}


class LoginPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Label(self, text='Username').grid(row=0, column=0, sticky='e', pady=5)
        username_entry = Entry(self)
        username_entry.grid(row=0, column=1, pady=5)
        Label(self, text='Password').grid(row=1, column=0, sticky='e', pady=5)
        password_entry = Entry(self, show='*')
        password_entry.grid(row=1, column=1, pady=5)
        ttk.Button(self, text='Go Back', command=lambda: controller.show_frame(MenuPage)).grid(row=2, column=0, pady=5)
        ttk.Button(self, text='Login', command=lambda: send_data(data_dict)).grid(row=2, column=1, pady=5)
        data_dict = {'request': 'login', 'username': username_entry.get(), 'password': password_entry.get()}


class SearchPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        username = Entry(self)
        username.grid(row=0, column=0, pady=5)
        username.insert(0, 'Username...')
        ttk.Button(self, text='Search', command=lambda: send_data(data_dict)).grid(row=0, column=1, pady=5)
        ttk.Button(self, text='Go Back', command=lambda: controller.show_frame(MenuPage)).grid(row=1, column=0, pady=5)
        data_dict = {'request': 'request', 'for_user': username.get()}


class SearchResults(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        canvas = Canvas(self)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        y_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=canvas.yview)
        y_scrollbar.pack(side=RIGHT, fill=Y)
        x_scrollbar = ttk.Scrollbar(self, orient=HORIZONTAL, command=canvas.xview)  # x scrollbar not filling
        x_scrollbar.pack(side=BOTTOM, fill=X)
        canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        self.second_frame = Frame(canvas)
        canvas.create_window((0, 0), window=self.second_frame, anchor='nw')

    def show_results(self, result):
        for widget in self.second_frame.slaves():
            widget.destroy()
        self.second_frame.tkraise()
        Label(self.second_frame, text='Username').grid(row=0, column=0, padx=5)
        Label(self.second_frame, text='First Name').grid(row=0, column=1, padx=5)
        Label(self.second_frame, text='Last Name').grid(row=0, column=2, padx=5)
        Label(self.second_frame, text='Email').grid(row=0, column=3, padx=5)
        Label(self.second_frame, text='Gender').grid(row=0, column=4, padx=5)
        Label(self.second_frame, text='Date Of Birth').grid(row=0, column=5, padx=5)
        row = 1
        for user in result:
            column = 0
            for field in user:
                Label(self.second_frame, text=field).grid(row=row, column=column, padx=5, pady=5)
                column += 1
            Button(self.second_frame, text='Message', command=lambda: None).grid(row=row, column=column, padx=5, pady=5)
            row += 1
        Button(self.second_frame, text='Go Back').grid(row=row, columnspan=6, sticky=N+S+E+W)

        
class ChatListWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        pass


class ChatWindow(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        pass

        
program = Program()


class ConnectionThread(threading.Thread):
    def __init__(self, socket, controller):
        threading.Thread.__init__(self)
        self.socket = socket
        self.controller = controller

    def run(self):
        while True:
            data = self.socket.recv(1024)
            if data == 0:
                break
            data = pickle.loads(data)
            response = data[0]

            if response == 'message':
                pass
            elif response == 'search_result':
                result = data[1]
                self.controller.show_frame(SearchResults)
                search_controller = self.controller.frames_dict[SearchPage]
                search_controller.show_results(result)


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((host, port))
recieve_thread = ConnectionThread(socket, program)
recieve_thread.start()


def send_message(to_user, message):
    data_dict = {'request': 'message', 'to_user': to_user, 'message': message}
    send_data(data_dict)


def send_data(data):
    socket.send(pickle.dumps(data))


mainloop()
