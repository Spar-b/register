from Utils import stats


class RegisterDate:
    def __init__(self):
        print("RegisterDate instance created")
        
    @staticmethod
    def save_all(data, db):
        cursor = db.db.cursor()
        
        for i in range(len(data)):
            print(data[i])
            if data[i] is None or data[i] == '' or data[i] == ' ':
                continue

            sql_query = f'''
                        INSERT INTO register_dates(group_id, subject_id, date_value, date_num) VALUES({stats.current_parent_id}, {stats.current_subject_id}, '{data[i]}', {i});
            '''
            cursor.execute(sql_query)
        db.db.commit()
        print("Successfull dates save")