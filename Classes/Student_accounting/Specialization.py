class Specialization:
    def __init__(self, id, name, department_id):
        self.id = id
        self.name = name
        self.department_id = department_id

    @staticmethod
    def to_child(id):
        sql_query = f'''
            SELECT id FROM years WHERE specialization_id = {id};
        '''
        from Utils import stats
        stats.current_table = "years"
        print("Specializations --> Years")
        return sql_query
