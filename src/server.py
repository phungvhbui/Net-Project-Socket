import socket
import threading

# constant values
PORT = 5050
HOST = socket.gethostbyname(socket.gethostname())
ADDR = (HOST, PORT)

HEADER = 64
FORMAT = "utf-8"
DISCONNECT_MSG = "!"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind(ADDR)

def start():
    server.listen()
    print(socket.SOMAXCONN)
    print(f"[LISTENING] Server is listening on {HOST}\n")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTION] {threading.activeCount() - 1}\n")

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                print(f"Client {addr} is disconnecting.\n")
                break

            print(f"[RECEIVED DATA] {addr} : {msg}\n")

    conn.close()

print("[STARTING] Server is starting...\n")
start()