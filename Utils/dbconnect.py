import mysql.connector
import atexit


class DBConnect:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="courseproject"
        )
        self.cursor = self.db.cursor()

        atexit.register(self.cleanup)

    def cleanup(self):
        self.cursor.close()
        self.db.close()

    def execute_query(self, query):
        self.cursor.execute(query)
        self.db.commit()
        data = self.cursor.fetchall()
        return data
