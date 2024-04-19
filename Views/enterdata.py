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
        self.sql_query = f'''
            SELECT subject.id, subject.subject_name
            FROM account_subject
            JOIN subject ON account_subject.subject_id = subject.id
            WHERE account_subject.account_id = {stats.current_user.id};
        '''
        self.column_names = []
        stats.current_user.subjects = self.populate_table(self.cursor, self.sql_query)
        print(stats.current_user.subjects)

        self.table.grid(row=0, column=0, columnspan=8)
        empty_row = [""] * self.table.columns
        #self.table.add_row(empty_row)
        stats.current_table = "subjects"

    def add_empty_row(self):
        # Error with adding a row to the table after switched content_frame at least once
        empty_row = [""] * self.table.columns
        stats.table_data.append(empty_row)
        self.table.add_row(empty_row)

    def populate_table(self, cursor, query):
        # Execute the SQL query
        cursor.execute(query)

        # Fetch data from the cursor
        data = cursor.fetchall()
        print(f"Data: {data}")

        # Get the column names from the cursor description
        self.column_names = [desc[0] for desc in cursor.description]
        print(f"Column names: {self.column_names}")
        num_columns = len(self.column_names)

        # Convert data to a 2D array
        stats.table_data = [self.column_names]  # Set the first row as column headers
        stats.table_data.extend([[str(value) for value in row] for row in data])  # Append the actual data

        array = stats.table_data[1:]
        print(f"Table data: {stats.table_data}")
        print(f"Array: {array}")

        # Clear the existing data in the table
        self.table.destroy()

        # Configure the table columns
        self.table = CTkTable(self, column=len(self.column_names), header_color=("#3a7ebf", "#1f538d"), values=stats.table_data, row=len(stats.table_data), command=self.table_on_click)
        self.table.grid(row=0, column=0, columnspan=8)
        print(self.table.values)

        self.table.headings = self.column_names
        return array

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
            popup.destroy()

        entry.bind("<Return>", save_and_close)
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)

    def save(self):
        print(stats.table_data)
        subject_data = stats.table_data[1:]
        try:
            db = DBConnect()
            cursor = db.db.cursor()
            subject_names = [name[1] for name in subject_data]
            ids = [id[0] for id in subject_data]
            print(ids)

            # Insert new subjects into the subjects table if they don't already exist
            for i in range(len(subject_names)):
                cursor.execute("""
                    INSERT INTO subject (id, subject_name)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY
                    UPDATE subject_name = VALUES(subject_name)
                """,
                               (ids[i], subject_names[i]))

            # Check if the account_id exists in the accounts table
            cursor.execute("SELECT id FROM accounts WHERE id = %s", (stats.current_user.id,))
            account_exists = cursor.fetchone()

            if account_exists:
                # Delete existing subjects for the user
                cursor.execute("DELETE FROM account_subject WHERE account_id = %s", (stats.current_user.id,))

                # Insert new subjects for the user
                for subject_id, _ in subject_data:
                    cursor.execute("INSERT INTO account_subject (account_id, subject_id) VALUES (%s, %s)",
                                   (stats.current_user.id, subject_id))

                db.db.commit()
                print("Subjects saved successfully for user with ID:", stats.current_user.id)
            else:
                print(f"Account with ID {stats.current_user.id} does not exist in the accounts table.")

            cursor.close()
        except Exception as e:
            print("Error saving subjects:", e)

    def to_child(self, cell):
        row = cell["row"]
        column = cell["column"]

        if row == 0:
            return

        from Classes import User_accounting, Student_accounting
        import Classes.Student_accounting.Department
        import Classes.Student_accounting.Specialization
        import Classes.Student_accounting.Year
        import Classes.Student_accounting.Group
        import Classes.Student_accounting.Student

        print(stats.table_data[row][0])
        id = stats.table_data[row][0]

        if stats.current_table == "students":
            self.sql_query = Classes.Student_accounting.Student.Student.to_child(id)
        if stats.current_table == "groups":
            self.sql_query = Classes.Student_accounting.Group.Group.to_child(id)
        if stats.current_table == "years":
            self.sql_query = Classes.Student_accounting.Year.Year.to_child(id)
        if stats.current_table == "specializations":
            self.sql_query = Classes.Student_accounting.Specialization.Specialization.to_child(id)
        if stats.current_table == "departments":
            self.sql_query = Classes.Student_accounting.Department.Department.to_child(id)
        if stats.current_table == "subjects":
            self.sql_query = Classes.User_accounting.Subject.Subject.to_child(id)

        print(stats.current_table)

        self.populate_table(self.cursor, self.sql_query)
        print("Succesful switch to child")

    def table_on_click(self, cell):
        if stats.tool_mode == "Edit":
            self.create_popup(cell)
        if stats.tool_mode == "Open":
            self.to_child(cell)

    @staticmethod
    def switch_to_edit():
        stats.tool_mode = "Edit"
        print("Switched to edit mode")
    @staticmethod
    def switch_to_open():
        stats.tool_mode = "Open"
        print("Switched to open mode")