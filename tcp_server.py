import socket

class TCPServer:
    def __init__(self, host, port, data_handler):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(1)
        self.data_handler = data_handler
    def start(self):
        print("Server is listening for connections...")
        while True:
            connection_socket, client_address = self.server_socket.accept()
            try:
                print(f"Connection from {client_address}")
                data = connection_socket.recv(1024).decode()
                print(f"Received: {data}")
                received_integers = eval(data)
                self.data_handler(received_integers)
            finally:
                connection_socket.close()
