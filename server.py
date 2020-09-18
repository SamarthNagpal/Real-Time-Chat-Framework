import socket
import threading
import mysql.connector
import pickle
import random
import smtplib
import os

host = ''
port = 9999

MY_ADDRESS = ''
MY_PASSWORD = ''

sql_host = 'localhost'
sql_user = 'root'
sql_password = '123'
sql_database = 'server'
sql_table = 'users'


mydb = mysql.connector.connect(host=sql_host, user=sql_user, passwd=sql_password)
my_cursor = mydb.cursor()
my_cursor.execute('SHOW DATABASES')
if (sql_database, ) not in my_cursor.fetchall():
    my_cursor.execute(f'CREATE DATABASE {sql_database}')
    mydb.database = sql_database
else:
    mydb.database = sql_database
my_cursor.execute('SHOW TABLES')
if (sql_table, ) not in my_cursor.fetchall():
    my_cursor.execute(f'CREATE TABLE {sql_table} (first_name VARCHAR(255), last_name VARCHAR(255), email VARCHAR(255),username VARCHAR(255), password VARCHAR(255), gender VARCHAR(40), dob VARCHAR(40))')


project_directory = os.getcwd()
if not os.path.isdir('./pending_messages'):
    fp = os.path.join(project_directory, 'pending_messages')
    os.mkdir(fp)


class ConnectionThread(threading.Thread):
    def __init__(self, conn, address):
        threading.Thread.__init__(self)
        self.conn = conn
        self.address = address

    def send_mail(self, email_address):
        self.code = str(random.randint(100000, 999999))
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(MY_ADDRESS, MY_PASSWORD)
            subject = 'Email Verification'
            body = f'Your email verification code: {self.code}'
            msg = f'Subject: {subject}\n\n{body}'
            server.sendmail(MY_ADDRESS, email_address, msg)

    def code_verification(self, code):
        if code == self.code:
            self.register_profile(self.details)
            self.conn.send(bytes('verified', 'utf-8'))
        else:
            self.conn.send(bytes('not verified', 'utf-8'))

    def register_profile(self, details):
        query = f'INSERT INTO {sql_table} {details}'
        with threading.Lock():
            my_cursor.execute(query)
            mydb.commit()
            clients_dict[details[3]] = self.conn

    def login(self, username, password):
        with threading.Lock():
            query = f'SELECT username, password FROM {sql_table} WHERE username={username}'
            my_cursor.execute(query)
            fetch = my_cursor.fetchall()
        if (username, password) in fetch:
            self.conn.send(bytes('verified', 'utf-8'))
            clients_dict[username] = self.conn
            self.username = username
            self.check_messages(self.username)
        else:
            self.conn.send(bytes('not verified', 'utf-8'))

    def check_messages(self, username):
        fp = os.path.join(project_directory, 'pending_messages')
        os.chdir(fp)
        if os.path.isfile(f'./{username}.txt'):
            try:
                lines_read = 0
                with open(f'{username}.txt', 'r') as file:
                    lines = file.readlines()
                for i in range(len(lines)):
                    line = lines[i]
                    line = line.split(':')
                    from_user = line[0]
                    message = ':'.join(line[1:])
                    send_data = ('message', from_user, message)
                    self.conn.send(pickle.dumps(send_data))
                    lines_read = i+1
            finally:
                self.save_messages(username, lines_read)

    def save_messages(self, username, variable):
        with threading.Lock():
            fp = os.path.join(project_directory, 'pending_messages')
            os.chdir(fp)
            if isinstance(variable, int):
                with open(f'{username}.txt', 'r') as file:
                    lines = file.readlines()
                with open(f'{username}.txt', 'w') as file:
                    new_lines = lines[variable:]
                    file.writelines(new_lines)
            elif isinstance(variable, str):
                with open(f'{username}.txt', 'a') as file:
                    file.write(variable)

    def search(self, username):
        with threading.Lock():
            query = f'SELECT first_name, last_name, email, username, gender, dob FROM {sql_table} WHERE username LIKE {username}%'
            my_cursor.execute(query)
            fetch = my_cursor.fetchall()
        send_data = ('search_result', fetch)
        self.conn.send(pickle.dumps(send_data))

    def run(self):
        while True:
            data = self.conn.recv(1024)
            if data == 0:
                break
            data = pickle.loads(data)
            request = data['request']

            if request == 'register':
                with threading.Lock():
                    query = f'SELECT * FROM {sql_table} WHERE email={data["data"[2]]}'
                    my_cursor.execute(query)
                    if my_cursor.rowcount != 0:
                        self.conn.send(bytes('invalid email', 'utf-8'))
                    else:
                        query = f'SELECT * FROM {sql_table} WHERE username={data["data"[3]]}'
                        my_cursor.execute(query)
                        if my_cursor.rowcount != 0:
                            self.conn.send(bytes('invalid username', 'utf-8'))
                        else:
                            self.details = data['data']
                            self.email = data['data'][2]
                            self.send_mail(self.email)
                            self.username = data['data'][3]

            elif request == 'verification':
                self.code_verification(data['code'])

            elif request == 'resend':
                self.send_mail(self.email)

            elif request == 'login':
                self.login(data['username'], data['password'])

            elif request == 'message':
                to_user = data['to_user']
                message = data['message']
                if to_user in clients_dict:
                    send_data = ['message', self.username, message]
                    clients_dict[to_user].send(pickle.dumps(send_data))
                else:
                    self.save_messages(to_user, f'{self.username}:{message}')

            elif request == 'search':
                self.search(data['username'])


clients_dict = {}
server_socket = socket.socket()
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(3)
while True:
    connection, address = server_socket.accept()
    client_thread = ConnectionThread(connection, address)
    client_thread.start()
