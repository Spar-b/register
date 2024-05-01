from Utils import stats
import CTkTable
from Views.Table_operations import TableOperations


class Table_population:
    def __init__(self):
        print("Table population class created")

    @staticmethod
    def populate_students_table(master):
        sql_query = f'''
                        SELECT name FROM students WHERE group_id = {stats.current_parent_id};
                '''
        master.cursor.execute(sql_query)
        student_data = master.cursor.fetchall()
        student_list = [(idx + 1, name[0], *(None,) * 25) for idx, name in enumerate(student_data)]

        # Add headings
        column_names = ['№', 'ПІБ студента'] + [' '] * 25

        # Combine headings and student_list
        stats.table_data = [column_names] + student_list

        master.table.destroy()


        master.table = CTkTable.CTkTable(master, column=len(column_names), header_color=("#3a7ebf", "#1f538d"),
                              values=stats.table_data, row=len(stats.table_data), command=master.table_on_click)

        master.table.pack(fill='both', expand=True)

        print(f"Table data: {stats.table_data}")


    @staticmethod
    def populate_table(master, query):
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
