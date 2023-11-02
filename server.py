# Server

import socket
import select

def receive_message(client_socket):
    try:
        message = client_socket.recv(1024).decode()
        if not message:
            return False
        return message
    except:
        return False

# Prompt the user for server address and port
server_ip = input("Enter the server IP address: ")
server_port = int(input("Enter the server port: "))

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Define server address and port based on user input
server_address = (server_ip, server_port)
server_socket.bind(server_address)
server_socket.listen(5)

sockets_list = [server_socket]
clients = {}

print("Server is running on {}:{}".format(server_ip, server_port))

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print("Accepted connection from {}:{}".format(client_address[0], client_address[1]))
        else:
            message = receive_message(notified_socket)
            if message is False:
                print("Closed connection from {}".format(clients[notified_socket]))
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user = clients[notified_socket]
            print(f"Received message from {user}: {message}")
            for client_socket in clients:
                if client_socket != notified_socket:
                    client_socket.send(f"{user}: {message}".encode())
