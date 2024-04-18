class Year:
    def __init__(self, id, specialization_id):
        self.id = id
        self.specialization_id = specialization_id

    @staticmethod
    def to_child(id):
        sql_query = f'''
                SELECT id, name FROM groups WHERE year_id = {id};
            '''
        from Utils import stats
        stats.current_table = "groups"
        print("Years --> Groups")
        return sql_query
