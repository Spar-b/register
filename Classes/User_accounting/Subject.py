from Utils import stats as stats


class Subject:
    def __init__(self, id, subject_name):
        self.id = id
        self.subject_name = subject_name
        self.users = []
        self.departments = []

    @staticmethod
    def get_all_for_user(id):
        sql_query = f'''
                    SELECT subjects.id AS '№', subjects.subject_name AS 'Назва предмету'
                    FROM account_subject
                    JOIN subjects ON account_subject.subject_id = subjects.id
                    WHERE account_subject.account_id = {id};
                '''
        return sql_query
    @staticmethod
    def save_all(subject_data, db):
        cursor = db.db.cursor()
        for subject_id, subject_name in subject_data:
            cursor.execute(
                f"INSERT INTO subjects (id, subject_name) VALUES (%s, %s) ON DUPLICATE KEY UPDATE subject_name = VALUES(subject_name);"
                , (subject_id, subject_name))

        cursor.execute("DELETE FROM account_subject WHERE account_id = %s", (stats.current_user.id,))

        db.db.commit()

        print(f"Current user id: {stats.current_user.id}")

        for subject_id, _ in subject_data:
            print(f"Subject id: {subject_id}")
            cursor.execute("INSERT INTO account_subject (account_id, subject_id) VALUES (%s, %s);",
                           (stats.current_user.id, subject_id))
        print("Succesfully saved to Subjects")

        db.db.commit()

    @staticmethod
    def to_child(id):
        sql_query = f'''
            SELECT d.*
            FROM departments d
            JOIN subject_department sd ON d.id = sd.department_id
            JOIN subjects s ON sd.subject_id = s.id
            WHERE s.id = {id};
        '''
        from Utils import stats
        stats.current_table = "departments"
        print("Subjects --> Departments")

        return sql_query
