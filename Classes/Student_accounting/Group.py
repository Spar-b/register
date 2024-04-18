class Group:
    def __init__(self, id, year_id):
        self.id = id
        self.year_id = year_id
        self.students = []

    @staticmethod
    def to_child(id):
        sql_query = f'''
                    SELECT id, name FROM students WHERE group_id = {id};
                '''
        from Utils import stats
        stats.current_table = "students"
        print("Groups --> Students")
        return sql_query
