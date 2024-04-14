class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.subjects = []

    def get_all_from_db(self):
        from Utils.dbconnect import DBConnect
        db = DBConnect()
        data = db.execute_query("SELECT * FROM accounts;")
        table_data =[[str(value) for value in row] for row in data]
