import psycopg2 as ps

class DatabaseManager:
    def __init__(self, host, port, database, user, password):
        self.connection = ps.connect(host=host, port=port, database=database, user=user, password=password)
        self.crsr = self.connection.cursor()

    def insert_data(self, data):
        self.crsr.execute("INSERT INTO customers VALUES (%s, %s, %s, %s)", tuple(data))
        self.connection.commit()

    def close(self):
        self.crsr.close()
        self.connection.close()
