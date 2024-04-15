import customtkinter
from CTkTable import CTkTable
import mysql.connector
from Utils.dbconnect import DBConnect


class EnterData(customtkinter.CTkScrollableFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        db = DBConnect()
        cursor = db.db.cursor()

        self.table = CTkTable(self, column=1, row=1)
        sql_query = f'''
            SELECT subject.id, subject.subject_name
            FROM account_subject
            JOIN subject ON account_subject.subject_id = subject.id
            WHERE account_subject.account_id = 1;
        '''
        self.column_names = []
        self.table_data = []
        self.populate_table(cursor, sql_query)

        self.table.grid(row=0, column=0, columnspan=8)

    def add_empty_row(self):
        # Error with adding a row to the table after switched content_frame at least once
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
