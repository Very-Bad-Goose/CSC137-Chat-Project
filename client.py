# Client

import socket
import sys
import threading

def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Connection closed.")
            client_socket.close()
            sys.exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Prompt the user for server IP and port
server_ip = input("Enter the server IP address: ")
server_port = int(input("Enter the server port: "))

server_address = (server_ip, server_port)
client_socket.connect(server_address)

# Prompt the user to enter their name
user = input("Enter your name: ")
client_socket.send(user.encode())

# Create two threads for sending and receiving messages
send_thread = threading.Thread(target=send_message, args=(client_socket,))
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))

send_thread.start()
receive_thread.start()
