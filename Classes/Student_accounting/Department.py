class Department:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.specializations = []

    @staticmethod
    def to_child(id):
        sql_query = f'''
            SELECT id, name FROM specializations WHERE department_id = {id};
        '''
        from Utils import stats
        stats.current_table = "specializations"
        print("Departments --> Specializations")
        return sql_query
