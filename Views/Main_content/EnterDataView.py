import customtkinter
from CTkTable import CTkTable

from Utils.dbconnect import DBConnect
from Utils import stats as stats
from Views.Main_content.Table_operations.Table_population import Table_population


class EnterData(customtkinter.CTkScrollableFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.table_population = Table_population()

        self.db = DBConnect()
        self.cursor = self.db.db.cursor()

        self.table = CTkTable(self, column=1, row=1)
        from Classes.User_accounting.Subject import Subject
        self.sql_query = Subject.get_all_for_user(stats.current_user.id)
        self.column_names = []
        stats.current_user.subjects = self.table_population.populate_table(self, self.sql_query)
        print(stats.current_user.subjects)

        self.table.grid(row=0, column=0, columnspan=8)
        stats.current_table = "subjects"

    def table_on_click(self, cell):
        from Views.Main_content.Table_operations.Table_operations import TableOperations
        match stats.tool_mode:
            case 'Edit':
                TableOperations.create_popup(self, cell)
            case 'Open':
                stats.current_parent_id = stats.table_data[cell["row"]][0]
                print(f"Current parent id: {stats.current_parent_id}")
                TableOperations.to_child(self, cell)
            case 'Delete':
                id_to_delete = stats.table_data[cell["row"]][0]
                TableOperations.delete_item(self, id_to_delete)

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

    @staticmethod
    def refresh_save_stats():
        stats.table_saved = False
        stats.edits_made = False
