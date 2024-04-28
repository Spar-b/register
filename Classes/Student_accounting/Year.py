from Utils import stats

class Year:
    def __init__(self, id, specialization_id):
        self.id = id
        self.specialization_id = specialization_id

    @staticmethod
    def to_child(id):
        sql_query = f'''
                SELECT id, name FROM groups WHERE year_id = {id};
            '''
        stats.current_table = "groups"
        print("Years --> Groups")
        return sql_query

    @staticmethod
    def save_all(data, db):
        cursor = db.db.cursor()
        print(data)
        for item in data:
            for id in item:
                cursor.execute(
                    f"INSERT INTO years (id, specialization_id) VALUES (%s, %s) ON DUPLICATE KEY UPDATE specialization_id = VALUES(specialization_id);"
                    , (id, stats.current_parent_id))

        print("Successfully saved Years")
        db.db.commit()
