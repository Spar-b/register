from Utils import stats

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
        stats.current_table = "years"
        print("Specializations --> Years")
        return sql_query

    @staticmethod
    def save_all(data, db):
        cursor = db.db.cursor()
        for id, name in data:
            cursor.execute(
                f"INSERT INTO specializations (id, department_id, name) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name);"
                , (id, stats.current_parent_id, name))

        print("Successfully saved Specializations")
        db.db.commit()
