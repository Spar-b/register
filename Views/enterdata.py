import customtkinter
from CTkTable import CTkTable
import mysql.connector
from Utils.dbconnect import DBConnect


class EnterData(customtkinter.CTkScrollableFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        db = DBConnect()
        cursor = db.db.cursor()

        self.table = CTkTable(self, column=1, row=1)
        self.populate_table(cursor, "accounts")

        self.table.grid(row=0, column=0, columnspan=8)

    def populate_table(self, cursor, table_name):
        # Execute the SQL query
        sql_query = f'''
            SELECT * FROM {table_name};
        '''
        cursor.execute(sql_query)

        # Fetch data from the cursor
        data = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]
        num_columns = len(column_names)

        # Convert data to a 2D array
        self.table_data = [column_names]  # Set the first row as column headers
        self.table_data.extend([[str(value) for value in row] for row in data])  # Append the actual data

        # Clear the existing data in the table
        for i in range(0, self.table.rows):
            self.table.delete_row(0)

        # Configure the table columns
        self.table = CTkTable(self, column=len(column_names), header_color=("#3a7ebf", "#1f538d"), values=self.table_data, row=len(self.table_data))

        # Set the column headings
        self.table.headings = column_names
