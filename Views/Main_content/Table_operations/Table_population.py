from Utils import stats
import CTkTable


class Table_population:
    def __init__(self):
        print("Table population class created")

    @staticmethod
    def populate_students_table(master):
        master.app.navbar_absent_button.configure(state='normal')
        sql_query = f'''
                        SELECT id, name FROM students WHERE group_id = {stats.current_parent_id};
                '''
        master.cursor.execute(sql_query)
        student_data = master.cursor.fetchall()
        student_list = [[idx + 1, name[1]] for idx, name in enumerate(student_data)]

        grade_list=[]
        print(student_data)
        for row in student_data:
            sql_query = f'''
                        SELECT grade_value, grade_num FROM grades WHERE student_id = {row[0]}
            '''
            master.cursor.execute(sql_query)
            grade_data = master.cursor.fetchall()
            print(grade_data)
            grade_row = []
            for i in range(stats.default_register_column_count):
                grade_found = False
                for grade_value, grade_num in grade_data:
                    if grade_num == i:
                        if i < len(grade_row):
                            print(grade_row[i])
                        else:
                            grade_row.append(grade_value)
                            grade_found = True
                if not grade_found:
                    grade_row.append(None)

            grade_list.append(grade_row)

            print(grade_list)

        # Add headings
        column_names = ['№', 'ПІБ студента'] + [' '] * stats.default_register_column_count

        # Combine student_list and grade_list
        combined_data = []
        for student, grades in zip(student_list, grade_list):
            combined_data.append(student + grades)

        # Add headings
        combined_data.insert(0, column_names)

        # Assign to stats.table_data
        stats.table_data = combined_data

        master.table.destroy()


        master.table = CTkTable.CTkTable(master, column=len(column_names), header_color=("#3a7ebf", "#1f538d"),
                              values=stats.table_data, row=len(stats.table_data), command=master.table_on_click)

        master.table.edit_column(1, width=380)

        master.table.pack(fill='both', expand=True)

        print(f"Table data: {stats.table_data}")


    @staticmethod
    def populate_table(master, query):
        try:
            master.app.navbar_absent_button.configure(state='disabled')
        except AttributeError:
            print("Can't change absent button state")
        master.cursor.execute(query)

        data = master.cursor.fetchall()
        print(f"Data: {data}")

        column_names = [desc[0] for desc in master.cursor.description]
        print(master.cursor.description)
        print(f"Column names: {column_names}")
        num_columns = len(column_names)

        stats.table_data = [column_names]
        stats.table_data.extend([[str(value) for value in row] for row in data])

        array = stats.table_data[1:]

        master.table.destroy()

        master.table = CTkTable.CTkTable(master, column=len(master.column_names), header_color=("#3a7ebf", "#1f538d"), values=stats.table_data, row=len(stats.table_data), command=master.table_on_click)
        master.table.grid(row=0, column=0, columnspan=8)

        print(f"Stats data: {stats.table_data}")
        print(f"Table data: {master.table.values}")
        print(f"Array: {array}")

        master.table.headings = master.column_names
        return array
