import customtkinter
from CTkTable import CTkTable
import mysql.connector

import Classes.User_accounting.Subject
from Utils.dbconnect import DBConnect
from Utils import stats as stats


class EnterData(customtkinter.CTkScrollableFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.db = DBConnect()
        self.cursor = self.db.db.cursor()

        self.table = CTkTable(self, column=1, row=1)
        from Classes.User_accounting.Subject import Subject
        self.sql_query = Subject.get_all_for_user(stats.current_user.id)
        self.column_names = []
        stats.current_user.subjects = self.populate_table(self.cursor, self.sql_query)
        print(stats.current_user.subjects)

        self.table.grid(row=0, column=0, columnspan=8)
        stats.current_table = "subjects"

    def add_empty_row(self):
        empty_row = [""] * self.table.columns
        stats.table_data.append(empty_row)
        self.table.add_row(empty_row)

        if len(stats.table_data) != len(self.table.values):
            stats.table_data = stats.table_data[:-1]
        print(f"Stats data: {stats.table_data}")
        print(f"Table data: {self.table.values}")
        print(" ")


    def populate_table(self, cursor, query):
        cursor.execute(query)

        data = cursor.fetchall()
        print(f"Data: {data}")

        self.column_names = [desc[0] for desc in cursor.description]
        print(cursor.description)
        print(f"Column names: {self.column_names}")
        num_columns = len(self.column_names)

        stats.table_data = [self.column_names]
        stats.table_data.extend([[str(value) for value in row] for row in data])

        array = stats.table_data[1:]

        self.table.destroy()

        self.table = CTkTable(self, column=len(self.column_names), header_color=("#3a7ebf", "#1f538d"), values=stats.table_data, row=len(stats.table_data), command=self.table_on_click)
        self.table.grid(row=0, column=0, columnspan=8)

        print(f"Stats data: {stats.table_data}")
        print(f"Table data: {self.table.values}")
        print(f"Array: {array}")

        self.table.headings = self.column_names
        return array

    def populate_students_table(self):
        sql_query = f'''
                        SELECT name FROM students WHERE group_id = {stats.current_parent_id};
                '''
        self.cursor.execute(sql_query)
        student_data = self.cursor.fetchall()
        student_list = [(idx + 1, name[0], *(None,) * 25) for idx, name in enumerate(student_data)]

        # Add headings
        self.column_names = ['№', 'ПІБ студента'] + [' '] * 25

        # Combine headings and student_list
        stats.table_data = [self.column_names] + student_list

        self.table.destroy()

        self.table = CTkTable(self, column=len(self.column_names), header_color=("#3a7ebf", "#1f538d"),
                              values=stats.table_data, row=len(stats.table_data), command=self.table_on_click)

        self.table.pack(fill='both', expand=True)

        print(f"Table data: {stats.table_data}")
    def create_popup(self, cell):
        row = cell["row"]
        column = cell["column"]

        if row == 0:
            return

        popup = customtkinter.CTkToplevel()
        popup.title("Edit Cell")
        popup.grab_set()

        entry = customtkinter.CTkEntry(popup)
        entry.pack(padx=10, pady=10)

        def save_and_close(event=None):
            new_value = entry.get()
            stats.table_data[row][column] = new_value
            self.table.update_values(stats.table_data)
            stats.edits_made = True
            popup.destroy()

        entry.bind("<Return>", save_and_close)
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)

    def save(self):
        data = stats.table_data[1:]
        print(f"save_data: {data}")
        match stats.current_table:
            case "subjects":
                from Classes.User_accounting.Subject import Subject
                from Classes.Misc.UserSubject import UserSubject
                for row in data:
                    subject = Subject(row[0], row[1])
                    user_subject = UserSubject(stats.current_user.id, row[0])
                    stats.local_tables.subjects.append(subject)
                    stats.local_tables.user_subjects.append(user_subject)

                    Subject.save_all(data, self.db)
                    stats.table_saved = True

            case "departments":
                from Classes.Student_accounting.Department import Department
                from Classes.Misc.SubjectDepartment import SubjectDepartment
                for row in data:
                    department = Department(row[0], row[1])
                    subject_department = SubjectDepartment(stats.current_parent_id, row[0])
                    stats.local_tables.departments.append(department)
                    stats.local_tables.subject_departments.append(subject_department)

                    Department.save_all(data, self.db)
                    stats.table_saved = True

            case "specializations":
                from Classes.Student_accounting.Specialization import Specialization
                for row in data:
                    specialization = Specialization(row[0], row[1], stats.current_parent_id)
                    stats.local_tables.specializations.append(specialization)

                    Specialization.save_all(data, self.db)
                    stats.table_saved = True

            case "years":
                from Classes.Student_accounting.Year import Year
                for row in data:
                    year = Year(row[0], stats.current_parent_id)
                    stats.local_tables.years.append(year)

                    Year.save_all(data, self.db)
                    stats.table_saved = True

            case "student_groups":
                import Classes.Student_accounting.Group as Group
                for row in data:
                    group = Group.Group(row[0], stats.current_parent_id)
                    stats.local_tables.groups.append(group)

                    Group.Group.save_all(data, self.db)
                    stats.table_saved = True

            case "students":
                from Classes.Student_accounting.Student import Student
                for row in data:
                    student = Student(row[0], row[1], stats.current_parent_id)
                    if len(row) == 4:
                        student.email = row[3]
                    stats.local_tables.students.append(student)

        stats.local_tables.print_all()

    def to_child(self, cell):
        row = cell["row"]
        column = cell["column"]

        if row == 0:
            return

        import Classes
        import Classes.Student_accounting
        import Classes.Student_accounting.Group
        import Classes.Student_accounting.Year
        import Classes.Student_accounting.Specialization
        import Classes.Student_accounting.Department

        print(stats.table_data[row][0])
        id = stats.table_data[row][0]

        match stats.current_table:
            case "student_groups":
                if stats.table_saved == stats.edits_made or stats.table_saved:
                    self.refresh_save_stats()
                    self.sql_query = Classes.Student_accounting.Group.Group.to_child(id)
                    self.populate_students_table()
                else:
                    self.table_not_saved_popup()

            case "years":
                if stats.table_saved == stats.edits_made or stats.table_saved:
                    self.refresh_save_stats()
                    self.sql_query = Classes.Student_accounting.Year.Year.to_child(id)
                else:
                    self.table_not_saved_popup()

            case "specializations":
                if stats.table_saved == stats.edits_made or stats.table_saved:
                    self.refresh_save_stats()
                    self.sql_query = Classes.Student_accounting.Specialization.Specialization.to_child(id)
                else:
                    self.table_not_saved_popup()

            case "departments":
                if stats.table_saved == stats.edits_made or stats.table_saved:
                    self.refresh_save_stats()
                    self.sql_query = Classes.Student_accounting.Department.Department.to_child(id)
                else:
                    self.table_not_saved_popup()

            case "subjects":
                if stats.table_saved == stats.edits_made or stats.table_saved:
                    self.refresh_save_stats()
                    self.sql_query = Classes.User_accounting.Subject.Subject.to_child(id)
                else:
                    self.table_not_saved_popup()

        print(stats.current_table)

        self.populate_table(self.cursor, self.sql_query)
        print("Succesful switch to child")

    def table_on_click(self, cell):
        match stats.tool_mode:
            case 'Edit':
                self.create_popup(cell)
            case 'Open':
                stats.current_parent_id = stats.table_data[cell["row"]][0]
                print(f"Current parent id: {stats.current_parent_id}")
                self.to_child(cell)
            case 'Delete':
                id_to_delete = stats.table_data[cell["row"]][0]
                self.delete_item(id_to_delete)

    def delete_item(self, id_to_delete):
        for row in stats.table_data:
            if row[0] == id_to_delete:
                stats.table_data.pop(int(id_to_delete))
                print(f"Item with id={id_to_delete} was successfully deleted")
                self.table.update_values(stats.table_data)
                self.table.delete_row(self.table.rows-1)
                stats.edits_made = True

    @staticmethod
    def switch_to_edit():
        stats.tool_mode = "Edit"
        print("Switched to edit mode")
    @staticmethod
    def switch_to_open():
        stats.tool_mode = "Open"
        print("Switched to open mode")

    @staticmethod
    def switch_to_delete():
        stats.tool_mode = "Delete"
        print("Switched to delete mode")

    def table_not_saved_popup(self):
        popup = customtkinter.CTkToplevel()
        popup.title("Edit Cell")
        popup.grab_set()

        label = customtkinter.CTkLabel(popup, text="Таблиця не збережена. Будь ласка збережіть зміни")
        label.pack(padx=10, pady=10)

        def ignore(popup):
            self.refresh_save_stats()
            popup.destroy()

        ignore_button = customtkinter.CTkButton(popup, text="Ігнорувати", command=lambda: ignore(popup))
        ignore_button.pack()

        popup.protocol("WM_DELETE_WINDOW", popup.destroy)

    def refresh_save_stats(self):
        stats.table_saved = False
        stats.edits_made = False
