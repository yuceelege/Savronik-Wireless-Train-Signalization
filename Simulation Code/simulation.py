import pandas as pd
import socket
import time
from datetime import datetime

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

def main():
    # Load the data
    df = pd.read_csv('modified_data.csv')  # Replace with your actual file path

    # Convert timestamps to datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Sort by timestamp just in case
    df.sort_values(by='timestamp', inplace=True)

    # Time scaling factor (1 second simulates 10 minutes, so 1 second = 600 seconds)
    time_scale = 600

    # Iterate through the DataFrame
    previous_timestamp = None
    for index, row in df.iterrows():
        if previous_timestamp is not None:
            # Calculate real-time delay
            time_diff = (row['timestamp'] - previous_timestamp).total_seconds() / time_scale
            time.sleep(time_diff)

        # Prepare and send the message
        msg = row.to_json()
        print(f"Sending: {msg}")
        send_message_to_server(msg)

        # Update the previous timestamp
        previous_timestamp = row['timestamp']

    print("Simulation complete.")

if __name__ == "__main__":
    main()
