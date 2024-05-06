from Utils import stats
import customtkinter


class TableOperations:
    def __init__(self):
        print("Table operations class created")
        
    @staticmethod
    def add_empty_row(master):
        empty_row = [""] * master.table.columns
        stats.table_data.append(empty_row)
        master.table.add_row(empty_row)

        if len(stats.table_data) != len(master.table.values):
            stats.table_data = stats.table_data[:-1]
        print(f"Stats data: {stats.table_data}")
        print(f"Table data: {master.table.values}")

    @staticmethod
    def create_popup(master, cell):
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
            master.table.update_values(stats.table_data)
            stats.edits_made = True
            popup.destroy()

        entry.bind("<Return>", save_and_close)
        popup.protocol("WM_DELETE_WINDOW", popup.destroy)

    @staticmethod
    def to_child(master, cell):
        row = cell["row"]
        column = cell["column"]

        if row == 0:
            return

        import Classes.User_accounting
        import Classes.Student_accounting
        import Classes.Student_accounting.Group
        import Classes.Student_accounting.Year
        import Classes.Student_accounting.Specialization
        import Classes.Student_accounting.Department

        print(stats.table_data[row][0])
        id = stats.table_data[row][0]

        if not (stats.table_saved == stats.edits_made or stats.table_saved):
            TableOperations.table_not_saved_popup(master)
            return

        from Views.Main_content.EnterDataView import EnterData
        EnterData.refresh_save_stats()

        match stats.current_table:
            case "student_groups":
                master.sql_query = Classes.Student_accounting.Group.Group.to_child(id)
                master.table_population.populate_students_table(master)
                return

            case "years":
                master.sql_query = Classes.Student_accounting.Year.Year.to_child(id)

            case "specializations":
                master.sql_query = Classes.Student_accounting.Specialization.Specialization.to_child(id)

            case "departments":
                master.sql_query = Classes.Student_accounting.Department.Department.to_child(id)

            case "subjects":
                master.sql_query = Classes.User_accounting.Subject.Subject.to_child(id)

        print(stats.current_table)

        master.table_population.populate_table(master, master.sql_query)
        print("Succesful switch to child")

    @staticmethod
    def delete_item(master, id_to_delete):
        for row in stats.table_data:
            try:
                if row[0] == id_to_delete:
                    stats.table_data.pop(int(id_to_delete))
                    print(f"Item with id={id_to_delete} was successfully deleted")
                    master.table.update_values(stats.table_data)
                    master.table.delete_row(master.table.rows-1)
                    stats.edits_made = True
            except ValueError:
                print(f"Incorrect type of id = {id_to_delete}")

    @staticmethod
    def table_not_saved_popup(master):
        popup = customtkinter.CTkToplevel()
        popup.title("Edit Cell")
        popup.grab_set()

        label = customtkinter.CTkLabel(popup, text="Таблиця не збережена. Будь ласка збережіть зміни")
        label.pack(padx=10, pady=10)

        def ignore():
            from Views.Main_content.EnterDataView import EnterData
            EnterData.refresh_save_stats()
            popup.destroy()

        ignore_button = customtkinter.CTkButton(popup, text="Ігнорувати", command=ignore)
        ignore_button.pack()

        popup.protocol("WM_DELETE_WINDOW", popup.destroy)