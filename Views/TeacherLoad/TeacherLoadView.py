import customtkinter
import CTkTable
from Views.Main_content.Table_operations.Table_population import Table_population
from Utils.dbconnect import DBConnect
from Utils import stats
from Classes.Misc.TeacherLoad import TeacherLoad
from Views.Main_content.EnterDataView import EnterData


class TeacherLoadView(EnterData):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        #self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        #self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        #self.table_population = Table_population()

        #self.db = DBConnect()
        #self.cursor = self.db.db.cursor()

        #self.table = CTkTable.CTkTable(self, column=1, row=1)
        self.sql_query = TeacherLoad.get_from_db()
        self.column_names = []
        stats.current_table = "teacher load"
        stats.current_user.subjects = self.table_population.populate_table(self, self.sql_query)
        print(stats.current_user.subjects)

        self.table.grid(row=0, column=0, columnspan=8)
