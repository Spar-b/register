from Utils import stats
import CTkTable

class Group:
    def __init__(self, id, year_id):
        self.id = id
        self.year_id = year_id
        self.students = []

    @staticmethod
    def to_child(id):
        sql_query = f'''
                    SELECT id, name FROM students WHERE group_id = {id}
        '''
        stats.current_table = "students"
        print("Groups --> Students")
        return sql_query

    @staticmethod
    def save_all(data, db):
        cursor = db.db.cursor()
        for id, name in data:
            cursor.execute(
                f"INSERT INTO student_groups (id, year_id, name) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name);"
                , (id, stats.current_parent_id, name))

        print("Successfully saved Groups")
        db.db.commit()