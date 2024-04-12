import customtkinter
from CTkTable import CTkTable
import mysql.connector


class EnterData(customtkinter.CTkScrollableFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1111",
            database="courseproject"
        )

        cursor = db.cursor()

        sql_query = '''
            SELECT * FROM accounts;
        '''

        cursor.execute(sql_query)

        self.table = CTkTable(self, column=15, row=3, header_color=("#3a7ebf", "#1f538d"))
        self.populate_table(cursor)

        cursor.close()
        db.close()

        self.table.grid(row=0, column=0, columnspan=8)

    def populate_table(self, cursor):
        # Fetch data from the cursor
        data = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [desc[0] for desc in cursor.description]

        # Clear the existing data in the table
        #for row in self.table.rows:
          #  self.table.delete_row(row)

        self.table.update_values([])

        i=0
        #while i < self.table.columns:
           # self.table.insert(0,i,column_names[i])
        # Configure the table columns
        #self.table.configure(columns=column_names)

        # Set the column headings
        self.table.headings = column_names

        # Populate the table with data
        for row_data in data:
            # Insert each cell value into the table
            self.table.insert(row=self.table.rows, values=[str(value) for value in row_data])

    def add_empty_row(self):
        new_row = [""] * self.table.columns
        self.table.insert(len(self.table.rows), 0, new_row)
