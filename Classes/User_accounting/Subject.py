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
                    SELECT subject.id, subject.subject_name
                    FROM account_subject
                    JOIN subject ON account_subject.subject_id = subject.id
                    WHERE account_subject.account_id = {id};
                '''
        return sql_query

    @staticmethod
    def to_child(id):
        sql_query = f'''
            SELECT d.*
            FROM departments d
            JOIN subject_department sd ON d.id = sd.department_id
            JOIN subject s ON sd.subject_id = s.id
            WHERE s.id = {id};
        '''
        from Utils import stats
        stats.current_table = "departments"
        print("Subjects --> Departments")

        return sql_query
