class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        self.subjects = []

    @staticmethod
    def get_all_from_db():
        from Utils.dbconnect import DBConnect
        db = DBConnect()
        data = db.execute_query("SELECT * FROM accounts;")
        user_list = []

        for row in data:
            user = User(*row)
            user_list.append(user)
        return user_list
