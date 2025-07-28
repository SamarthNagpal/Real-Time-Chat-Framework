# Real-Time Chat Framework

A Python-based real-time messaging application featuring a multi-threaded server and a Tkinter GUI client.  
Supports user registration with email verification, user search, and offline message delivery.

## Features
- **Real-time chat** with TCP sockets.
- **Concurrent clients** handled via multi-threaded server architecture.
- **Persistent user data** with MySQL database integration.
- **Email verification** for new users using SMTP.

## Tech Stack
- **Backend:** Python (socket, threading, pickle)
- **Frontend:** Tkinter (GUI)
- **Database:** MySQL
- **Other:** SMTP for email verification

## How It Works
1. The server manages all client connections and stores messages for offline users.
2. Clients can register, login, search users, and chat through the Tkinter interface.
3. Pending messages are delivered upon login.

## Future Improvements
- Group chat and message encryption.
- WebSocket or REST API interface.
- Improved GUI for better usability.
