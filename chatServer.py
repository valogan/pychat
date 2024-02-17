from socket import *
import threading

SIZE = 2048
MAX_MESSAGE_SIZE = 250
connections = []

class User:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
    def __str__(self):
        return str(self.addr) + " " + str(self.name)
    name = None
    channel = None
    connectionStatus = True
        

def doCommand(message, user):
    message = message.split(" ")
    if message[0] == "/NAME":
        newName = message[1].replace("\n","")
        if len(newName) > 20:
            user.conn.send("Name not set. Please pick a name 20 characters or less\n".encode())
            return
        user.name = newName
    elif message[0] == "/DISCONNECT":
        user.conn.close()
        print(f"[DISCONNECTION] {user} disconnected")
        connections.remove(user)
        user.connectionStatus = False
    elif message[0] == "/MSG":
        singlecast(message[1], message[2:], user)
    else:
        user.conn.send("command not found\n".encode())
        
    
def broadcast(message, user):
    for users in connections:
        if users.addr != user.addr:
            toSend = user.name + ": " + message + "\n"
            users.conn.send(toSend.encode())


def singlecast(name, message, user):
    if user.name:
        for users in connections:
            if name == users.name:
                finalMessage = ""
                for i in message:
                    finalMessage = finalMessage + i + " "
                finalMessage = finalMessage[:-1]
                finalMessage = user.name + " (private message): " + finalMessage + "\n"
                users.conn.send(finalMessage.encode())
                return
        user.conn.send(f"{name} not found\n".encode())
    else:
        user.conn.send("Message not sent. Please pick a name using \"/NAME\" command\n".encode())
    return

        
def handle_client(user):
    print(f"[NEW CONNECTION] {user.addr} connected.")
    user.conn.send("Welcome to the server!\n".encode())
    while True:
        data = user.conn.recv(SIZE).decode()
        if len(data) > MAX_MESSAGE_SIZE:
            continue
        data = data.replace("\r", "")
        data = data.replace("\n", "")
        print(f"{user}: {data}")
        if data[0] == "/":
            doCommand(data, user)
            if not user.connectionStatus:
                return
        else:
            if user.name:
                broadcast(data, user)
            else:
                user.conn.send("Please pick a name using \"/NAME\" command\n".encode())

                
def main():
    serverSocket = socket(AF_INET, SOCK_STREAM)
    IP = ""
    PORT = 6788
    ADDR = (IP, PORT)
    print("Server binding...")
    serverSocket.bind(ADDR)
    serverSocket.listen()
    print(f"Server listening on {ADDR}")
    while True:
        conn, addr = serverSocket.accept()
        user = User(conn, addr)
        connections.append(user)
        thread = threading.Thread(target = handle_client, args = (user,))
        thread.start()

if __name__ == "__main__":
    main()
