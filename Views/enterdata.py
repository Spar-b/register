import customtkinter
from CTkTable import CTkTable
import mysql.connector
from Utils.dbconnect import DBConnect
from Utils import stats as stats


class EnterData(customtkinter.CTkScrollableFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        db = DBConnect()
        cursor = db.db.cursor()

        self.table = CTkTable(self, column=1, row=1)
        self.sql_query = f'''
            SELECT subject.id, subject.subject_name
            FROM account_subject
            JOIN subject ON account_subject.subject_id = subject.id
            WHERE account_subject.account_id = 1;
        '''
        self.column_names = []
        self.table_data = []
        self.populate_table(cursor, self.sql_query)

        self.table.grid(row=0, column=0, columnspan=8)

    def add_empty_row(self):
        empty_row = [""] * self.table.columns
        self.table.add_row(values=empty_row)

    def populate_table(self, cursor, query):
        # Execute the SQL query
        cursor.execute(query)

        # Fetch data from the cursor
        data = cursor.fetchall()

        # Get the column names from the cursor description
        self.column_names = [desc[0] for desc in cursor.description]
        num_columns = len(self.column_names)

        # Convert data to a 2D array
        self.table_data = [self.column_names]  # Set the first row as column headers
        self.table_data.extend([[str(value) for value in row] for row in data])  # Append the actual data

        # Clear the existing data in the table
        for i in range(0, self.table.rows):
            self.table.delete_row(0)

        # Configure the table columns
        self.table = CTkTable(self, column=len(self.column_names), header_color=("#3a7ebf", "#1f538d"), values=self.table_data, row=len(self.table_data), command=self.create_popup)

        # Set the column headings
        self.table.headings = self.column_names

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
            self.table.insert(row, column, new_value)
            popup.destroy()

        entry.bind("<Return>", save_and_close)
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)

    def save(self, subject_data):
        try:
            db = DBConnect()
            cursor = db.db.cursor()
            # Insert new subjects into the subjects table if they don't already exist
            for subject_name in subject_data:
                cursor.execute(
                    "INSERT INTO subjects (subject_name) VALUES (%s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)",
                    (subject_name,))

            # Retrieve the last inserted ID for each subject
            cursor.execute("SELECT id FROM subjects WHERE subject_name IN %s", (tuple(subject_data),))
            subject_ids = cursor.fetchall()

            # Delete existing subjects for the user
            cursor.execute("DELETE FROM account_subject WHERE user_id = %s", (stats.current_user.id,))

            # Insert new subjects for the user
            for subject_id in subject_ids:
                cursor.execute("INSERT INTO account_subject (user_id, subject_id) VALUES (%s, %s)",
                               (stats.current_user.id, subject_id[0]))

            db.db.commit()
            cursor.close()
            print("Subjects saved successfully for user with ID:", stats.current_user.id)
        except Exception as e:
            print("Error saving subjects:", e)

    def get_table_data(self):
