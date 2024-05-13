from Classes.User_accounting.User import User
import Classes
from Utils.local_tables import LocalTables

no_account = User(0, "None", "None")
current_user = no_account
current_table = "subjects"
current_subject_id = -1
current_parent_id = -1
table_data = []
tool_mode = "Edit"
table_saved = False
edits_made = False
local_tables = LocalTables()
default_register_column_count = 20
current_register_page = 0
heading_rows_count = 1
