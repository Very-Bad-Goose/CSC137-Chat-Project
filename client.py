# Client
import os
import socket
import sys
import threading

def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())

        #exit back to command line if quit is issued
        if (message == "quit" or message == "QUIT"):
            print(f"{user} is quitting the chat server")
            os._exit(1)


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


if len(sys.argv) != 3:
    print("Invalid number of arguments supplied | Usage python3 client.py <svr_ip> <svr_port>")
    exit(1)
# check to make sure second argument (port) doesn't contain characters and is within usable range
if sys.argv[2].isnumeric() == False or int(sys.argv[2]) < 0 or int(sys.argv[2]) > 65535:
    print("invalid argument supplied: port must be numbers within the range 0-65535")
    exit(1)

# Output "JOIN" instructions and error check client
while True:
    firstCmd = input("Enter JOIN followed by your username: ")
    words = firstCmd.split()
    parsed_words = [word.lower() for word in words]
    # only break out of the condition checking if 2 args supplied and "join" is the first
    if (parsed_words[0] == "join") and (parsed_words[1]):
        break


# Take server IP and port from args
server_ip = sys.argv[1]        # input("Enter the server IP address: ")
server_port = int(sys.argv[2])      # int(input("Enter the server port: "))

server_address = (server_ip, server_port)
client_socket.connect(server_address)

# Prompt the user to enter their name
user = parsed_words[1]
client_socket.send(user.encode())

# Create two threads for sending and receiving messages
send_thread = threading.Thread(target=send_message, args=(client_socket,))
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))

send_thread.start()
receive_thread.start()
