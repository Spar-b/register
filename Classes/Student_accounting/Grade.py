from Utils import stats


class Grade:
    def __init__(self, id, student_id, value, time_graded, comment=""):
        self.id = id
        self.student_id = student_id
        self.value = value
        self.time_graded = time_graded
        self.comment = comment

    @staticmethod
    def save_all(data, db):
        cursor = db.db.cursor()

        for id, student_id, grade_num, grade_value in data:
            cursor.execute(
                f"INSERT INTO grades (id, student_id, grade_num, grade_value) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE grade_value = VALUES(grade_value), grade_num = VALUES(grade_num);"
                , (id, student_id, grade_num + stats.current_register_page * stats.default_register_column_count, grade_value))

        print("Successfully saved Students")
        db.db.commit()