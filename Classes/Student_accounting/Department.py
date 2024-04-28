from Utils import stats

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
        stats.current_table = "specializations"
        print("Departments --> Specializations")
        return sql_query
    
    @staticmethod
    def save_all(department_data, db):
        cursor = db.db.cursor()
        for id, name in department_data:
            cursor.execute(
                f"INSERT INTO departments (id, name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name);"
                , (id, name))

        cursor.execute("DELETE FROM subject_department WHERE subject_id = %s", (stats.current_parent_id,))


        for department_id, _ in department_data:
            print(f"Subject id: {department_id}")
            cursor.execute("INSERT INTO subject_department (subject_id, department_id) VALUES (%s, %s);",
                           (stats.current_parent_id, department_id))
        print("Succesfully saved to Departments")

        db.db.commit()
