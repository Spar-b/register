from Utils import stats
import CTkTable

class Group:
    def __init__(self, id, year_id):
        self.id = id
        self.year_id = year_id
        self.students = []

    @staticmethod
    def to_child(id):
        sql_query = f'''
                    SELECT s.name, g.grade_value
                    FROM students s
                    JOIN grades g ON s.id = g.student_id
                    WHERE s.group_id = {stats.current_parent_id};
                '''
        stats.current_table = "students"
        print("Groups --> Students")
        return sql_query

    @staticmethod
    def form_table(table, cursor, query, parent):
        cursor.execute(query)

        # Fetch data from the cursor
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        print(f"Column names: {column_names}")
        num_columns = len(column_names)

        # Convert data to a 2D array
        stats.table_data = [column_names]  # Set the first row as column headers
        stats.table_data.extend([[str(value) for value in row] for row in data])  # Append the actual data



    @staticmethod
    def save_all(data, db):
        cursor = db.db.cursor()
        for id, name in data:
            cursor.execute(
                f"INSERT INTO student_groups (id, year_id, name) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name);"
                , (id, stats.current_parent_id, name))

        print("Successfully saved Groups")
        db.db.commit()