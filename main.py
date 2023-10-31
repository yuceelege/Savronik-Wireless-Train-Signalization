from database_manager import DatabaseManager
from tcp_server import TCPServer

def main():
    db_manager = DatabaseManager(host="localhost", port="5432", database="master", user="postgres", password="GGGG2284")
    server = TCPServer(host='0.0.0.0', port=65432, data_handler=db_manager.insert_data)
    try:
        server.start()
    finally:
        db_manager.close()

if __name__ == "__main__":
    main()
