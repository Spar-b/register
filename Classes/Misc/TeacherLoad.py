from Utils import stats


class TeacherLoad:
    def __init__(self):
        print("TeacherLoad instance created successfully")

    @staticmethod
    def get_from_db():
        sql_query = f'''SELECT tl.id AS '№', s.subject_name AS 'Предмет', g.name AS 'Група', 
                    tl.lection_hours AS 'Лекції', tl.labs_hours AS 'Лаби', tl.exam_hours AS 'Екзамен', tl.weekly_hours AS 'В тиждень'
                    FROM teacher_load tl
                    JOIN subjects s ON tl.subject_id = s.id
                    JOIN student_groups g ON tl.group_id = g.id
                    WHERE tl.account_id = {stats.current_user.id} AND tl.subject_id = {stats.current_subject_id};'''
        return sql_query

    @staticmethod
    def save_to_db(data):
        from Utils.dbconnect import DBConnect
        db = DBConnect()
        cursor = db.cursor
        for row in data:
            values_string = f"{row[0]}, {stats.current_user}, {stats.current_subject_id}, {row[1]}, {row[2]}, {row[3]}, {row[4]}, {row[5]}"
            sql_query = f"INSERT INTO teacher_load VALUES ({values_string});"
            cursor.execute(sql_query)
