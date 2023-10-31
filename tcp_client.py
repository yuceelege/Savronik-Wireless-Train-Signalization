import socket
import time
import random

def send_message_to_server(message):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the server's port
    server_address = ('<SERVER_IP>', 65432)  # Replace <SERVER_IP> with the IP address of the server machine
    client_socket.connect(server_address)

    try:
        # Send the message
        client_socket.sendall(message.encode())
    finally:
        # Clean up the connection
        client_socket.close()

def generate_random_integers():
    return [random.randint(1, 100) for _ in range(4)]

if __name__ == "__main__":
    while True:
        random_integers = generate_random_integers()
        msg = str(random_integers)
        print(f"Sending: {msg}")
        send_message_to_server(msg)
        time.sleep(2)
