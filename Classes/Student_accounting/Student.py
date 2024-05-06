from Utils import stats


class Student:
    def __init__(self, id, name, group_id, email="None"):
        self.id = id
        self.name = name
        self.email = email
        self.group_id = group_id
        self.grades = []

    @staticmethod
    def to_child(id):
        sql_query = f'''
                        SELECT * FROM grades WHERE student_id = {id};
                    '''
        from Utils import stats
        stats.current_table = "grades"
        return sql_query

    @staticmethod
    def save_all(data, db):
        cursor = db.db.cursor()
        for id, name in data:
            cursor.execute(
                f"INSERT INTO students (id, group_id, name) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name);"
                , (id, stats.current_parent_id, name))

        print("Successfully saved Students")
        db.db.commit()
