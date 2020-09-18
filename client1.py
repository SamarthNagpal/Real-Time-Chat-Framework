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

        self.pages_list = [MenuPage, CreateProfilePage, EmailVerificationPage, LoginPage, SearchPage, SearchResults]
        self.frames = {}
        for F in self.pages_list:
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(EmailVerificationPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
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
            data = {'request': 'register', 'username': self.username, 'data': data_tuple}
            # send data
            print('hello')
            self.controller.show_frame(EmailVerificationPage)


class EmailVerificationPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        verification_code = Entry(self)
        verification_code.grid(row=1, column=0, pady=5)
        ttk.Button(self, text='Verify').grid(row=1, column=1, pady=5)
        ttk.Button(self, text='Go Back', command=lambda: controller.show_frame(CreateProfilePage)).grid(row=2, column=0, pady=5)
        ttk.Button(self, text='Resend Code').grid(row=2, column=1, pady=5)

        # sending code to server


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
        credential_tuple = (username_entry.get(), password_entry.get())
        data = {'request': 'login', 'username': username_entry.get(), 'login_credentials': credential_tuple}
        ttk.Button(self, text='Register').grid(row=2, column=1, pady=5)


class SearchPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        username = Entry(self)
        username.grid(row=0, column=0, pady=5)
        username.insert(0, 'Username...')
        ttk.Button(self, text='Search').grid(row=0, column=1, pady=5)
        ttk.Button(self, text='Go Back', command=lambda: controller.show_frame(MenuPage)).grid(row=1, column=0, pady=5)


class SearchResults(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        # show search results


program = Program()

mainloop()
