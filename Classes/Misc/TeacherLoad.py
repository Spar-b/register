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
                    WHERE tl.account_id = {stats.current_user.id};'''
        return sql_query

    @staticmethod
    def save_to_db(data):
        from Utils.dbconnect import DBConnect
        db = DBConnect()
        cursor = db.cursor
        for row in data:
            cursor.execute(f"SELECT id FROM student_groups WHERE name = '{row[2]}';")
            group_id = cursor.fetchone()[0]

            cursor.execute(f"SELECT id FROM subjects WHERE subject_name = '{row[1]}'")
            subject_id = cursor.fetchone()[0]

            values_string = f"{row[0]}, {stats.current_user.id}, {subject_id}, {group_id}, {row[3]}, {row[4]}, {row[5]}, {row[6]}"
            sql_query = f'''INSERT INTO teacher_load (id, account_id, subject_id, group_id, lection_hours, labs_hours, exam_hours, weekly_hours)
                        VALUES ({values_string})
                        ON DUPLICATE KEY UPDATE
                        account_id = VALUES(account_id),
                        subject_id = VALUES(subject_id),
                        group_id = VALUES(group_id),
                        lection_hours = VALUES(lection_hours),
                        labs_hours = VALUES(labs_hours),
                        exam_hours = VALUES(exam_hours),
                        weekly_hours = VALUES(weekly_hours);'''
            print(sql_query)
            cursor.execute(sql_query)
        db.db.commit()
