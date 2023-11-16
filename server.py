import socket
import select
import sys

def get_local_ip():
    # Get the local IP address of the server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Using UDP
        s.settimeout(0.1)
        s.connect(("10.255.255.255", 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = "127.0.0.1"  # Default to localhost if unable to determine IP
    return local_ip

def receive_message(client_socket): # Function helper for Direct messaging
    try:
        message = client_socket.recv(1024).decode()
        if not message:
            return False
        return message
    except:
        return False

def send_direct_message(sender_socket, recipient_username, message):
    # Find recipient's socket based on their username
    for client_socket, username in clients.items():
        if username == recipient_username:
            try:
                client_socket.send(f"Direct message from {sender_username}: {message}".encode())
            except:
                continue


if len(sys.argv) != 2:
    print("No port supplied | Usage python3 server.py *port number*")
    exit()
if (sys.argv[1].isnumeric() == False):
    print("port must be a valid number")
    exit()

inputPort = sys.argv[1]

# Get the local server IP address
server_ip = get_local_ip()
server_port = int(inputPort)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Define server address and port based on user input
server_address = (server_ip, server_port)
server_socket.bind(server_address)
server_socket.listen(5)

sockets_list = [server_socket]
clients = {}  # Used to map sockets to usernames

# Server welcome message on startup with the IP its running on
print("Server is running on {}:{}".format(server_ip, server_port))

while True:
    read_sockets, _, _ = select.select(sockets_list, [], [])
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, _ = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            sockets_list.append(client_socket)
            clients[client_socket] = user
            print(f"Accepted connection from {user}")
        else:
            message = receive_message(notified_socket)
            if message is False or message == "QUIT":
                sender_username = clients[notified_socket]
                print(f"Closed connection from {sender_username}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            # set commandisIssuedFlag back to 0 so others see messages
            commandisIssuedFlag = 0
            sender_username = clients[notified_socket]

            # Check if the message is a direct message
            if message.startswith("MESG "):
                parts = message.split(" ", 2)
                if len(parts) == 3:
                    recipient_username = parts[1].lower()
                    direct_message = parts[2]
                    send_direct_message(notified_socket, recipient_username, direct_message)
                    print(f"Direct message from {sender_username}: {direct_message}")
                    commandisIssuedFlag = 1

            # list out users to the requestor
            if message.startswith("LIST"):
                commandisIssuedFlag = 1
                connected_users = "\n ".join(clients.values())
                try:
                    notified_socket.send(f"Connected users:\n {connected_users}".encode())
                except:
                    continue

            # Message all in chatroom NOTE: commandisIssuedFlag = 0 means user did not type any "command" for the first arg
            # Message all in chatroom using broadcast
            if message.startswith("BCST "):
                commandisIssuedFlag = 1
                parts = message.split(" ", 1)
                message = parts[1]
                for client_socket in clients:
                    if client_socket != notified_socket:
                        try:
                            client_socket.send(f"{sender_username}: {message}".encode())
                            print(f"{sender_username} sent a message to all users containing: {message}")
                        except:
                            continue
            # Message was not sent with a command, error sent to user
            elif commandisIssuedFlag == 0:
                for client_socket in clients:
                    if client_socket == notified_socket:
                        try:
                            client_socket.send("Unknown Message".encode())
                            print(clients.get(client_socket) + " didn't use a command")
                        except:
                            continue