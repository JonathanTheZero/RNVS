import socket
import threading
import time
from enum import Enum


class ServerCode(Enum):
    EXT = -1
    ACK = 0
    UNKNOWN = 1


def server() -> None:
    server_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address: tuple[str, int] = ("localhost", 65432)
    print("[Server] Starting up on " + print_addr(server_address))
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)

    while True:
        print("[Server] Waiting for a connection")
        connection: socket.socket
        client_address: tuple[str, int]
        connection, client_address = server_socket.accept()
        try:
            print("[Server] Connection from", print_addr(client_address))

            while True:
                data: bytes = connection.recv(1024)
                if data:
                    str_data: str = data.decode()
                    print("[Server] Received:", str_data)

                    code, msg = server_parse_msg(str_data)
                    if code == ServerCode.EXT:
                        print("[Server] Initiating shutdown...")
                        return
                    else:
                        print(f"[Server] Flag: {code}, Message: {msg.decode("UTF-8")}")
                        connection.sendall(msg)
                else:
                    print("[Server] No more data from", print_addr(client_address))
                    break

        finally:
            connection.close()


def server_parse_msg(msg: str) -> tuple[ServerCode, bytes]:
    if msg == "exit":
        return (ServerCode.EXT, b"")
    if msg == "start":
        return (ServerCode.ACK, b"Acknowledged")

    return (ServerCode.UNKNOWN, b"Unknown protocol")


def client() -> None:
    client_socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address: tuple[str, int] = ("localhost", 65432)
    print("[Client] Connecting to " + print_addr(server_address))
    client_socket.connect(server_address)

    try:
        message: bytes = b"start"
        print("[Client] Sending:", message)
        client_socket.sendall(message)

        data: bytes = client_socket.recv(1024)
        print("[Client] Received acknowledgment:", data.decode())

        if data.decode() == "Acknowledged":
            message = b"Received acknowledgement, sending data now..."
            print("[Client] Sending data now...")
            client_socket.sendall(message)
            time.sleep(3)

    finally:
        print("[Client] Closing socket, telling server to shut down")
        message: bytes = b"exit"
        client_socket.sendall(message)
        client_socket.close()


def print_addr(addr_tup: tuple[str, int]) -> str:
    ip, port = addr_tup
    return f"{ip}:{port}"


if __name__ == "__main__":
    server_thread: threading.Thread = threading.Thread(target=server)
    server_thread.start()
    client()
