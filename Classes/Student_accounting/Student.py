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
