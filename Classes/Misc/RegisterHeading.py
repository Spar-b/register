from Utils import stats


class RegisterHeading:
    def __init__(self):
        print("Register Heading class instance created")

    @staticmethod
    def save_all(headings_data, db):
        cursor = db.db.cursor()
        for i in range(len(headings_data)):
            print(headings_data[i])
            if headings_data[i] is None or headings_data[i] == '' or headings_data[i] == ' ':
                continue

            sql_query = f'''
                        INSERT INTO register_headings(group_id, subject_id, heading_value, heading_num) VALUES({stats.current_parent_id}, {stats.current_subject_id}, '{headings_data[i]}', {i + stats.current_register_page * stats.default_register_column_count});
            '''
            cursor.execute(sql_query)
        db.db.commit()
        print("Successfull headings save")
