from Classes.User_accounting.User import User
from Utils.local_tables import LocalTables

no_account = User(0, "None", "None")
current_user = no_account
current_table = "subjects"
current_parent_id = -1
table_data = []
tool_mode = "Edit"
local_tables = LocalTables()
