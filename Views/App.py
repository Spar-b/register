import customtkinter
from Views.Main_content.EnterDataView import EnterData
from Views.Authorization.Login import Login
from Views.Authorization.Register import Register
from Views.Main_content.Table_operations.Table_operations import TableOperations
from Views.Main_content.Table_operations.Save_table import SaveTable

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Домашня сторінка")
        self.geometry(f"{1920}x{1080}")

        appearance_mode = customtkinter.get_appearance_mode()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid_rowconfigure(4, weight=1)

        self.content_frame = EnterData(self, fg_color=("#F5F5F5", "#000000"))
        self.content_frame.grid(row=1, column=1, sticky='nsew', rowspan=4)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Журнал учителя", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.authorization_button = customtkinter.CTkButton(self.sidebar_frame, command=self.to_authorization, text='Вихід з акаунту')
        self.authorization_button.grid(row=1, column=0, padx=20, pady=10)

        self.enter_data_button = customtkinter.CTkButton(self.sidebar_frame, command=self.to_enter_data, text='Ввід даних')
        self.enter_data_button.grid(row=2, column=0, padx=20, pady=10)

        self.teacher_load_button = customtkinter.CTkButton(self.sidebar_frame, command=self.to_teacher_load, text='Навантаження')
        self.teacher_load_button.grid(row=3, column=0, padx=20, pady=10)

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Тема:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Системна", "Світла", "Темна"],
                                                                       command=App.change_appearance_mode_event)
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="Масштаб:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionmenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%", "150%"],
                                                              command=self.change_scaling_event)
        self.scaling_optionmenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        self.navbar_frame = customtkinter.CTkFrame(self, corner_radius=0, height=100)
        self.navbar_frame.grid_rowconfigure((1, 2, 3), weight=1)
        self.navbar_frame.grid_columnconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20), weight=1)

        self.navbar_add_row_button = customtkinter.CTkButton(self.navbar_frame, text="Додати рядок", command=lambda: TableOperations.add_empty_row(self.content_frame))
        self.navbar_add_row_button.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.navbar_save_button = customtkinter.CTkButton(self.navbar_frame, text="Зберегти", font=customtkinter.CTkFont("Arial", 16), command= lambda: SaveTable.save(self.content_frame))
        self.navbar_save_button.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        self.navbar_edit_button = customtkinter.CTkButton(self.navbar_frame, text="Редагування",
                                                          command=EnterData.switch_to_edit)
        self.navbar_edit_button.grid(row=1, column=3, sticky="nsew", padx=10, pady=10)

        self.navbar_open_button = customtkinter.CTkButton(self.navbar_frame, text="Перехід",
                                                          command=EnterData.switch_to_open)
        self.navbar_open_button.grid(row=1, column=4, sticky="nsew", padx=10, pady=10)

        self.navbar_delete_button = customtkinter.CTkButton(self.navbar_frame, text="Видалення", font=customtkinter.CTkFont("Arial", 16), command=self.content_frame.switch_to_delete)
        self.navbar_delete_button.grid(row=1, column=5, sticky="nsew", padx=10, pady=10)

        self.navbar_absent_button = customtkinter.CTkButton(self.navbar_frame, text="нб", font=customtkinter.CTkFont("Arial", 16), command=self.content_frame.switch_to_absent, state='disabled')
        self.navbar_absent_button.grid(row=1, column=6, sticky="nsew", padx=10, pady=10)

        self.navbar_previous_page_button = customtkinter.CTkButton(self.navbar_frame, text="Минула сторінка",
                                                               font=customtkinter.CTkFont("Arial", 16),
                                                               command= lambda: self.content_frame.previous_page(self.content_frame),
                                                               state='disabled')
        self.navbar_previous_page_button.grid(row=1, column=7, sticky="nsew", padx=10, pady=10)

        self.navbar_next_page_button = customtkinter.CTkButton(self.navbar_frame, text="Наступна сторінка",
                                                               font=customtkinter.CTkFont("Arial", 16),
                                                               command= lambda: self.content_frame.next_page(self.content_frame),
                                                               state='disabled')
        self.navbar_next_page_button.grid(row=1, column=8, sticky="nsew", padx=10, pady=10)

        self.to_authorization()

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):

        match new_appearance_mode:
            case 'Світла':
                customtkinter.set_appearance_mode("Light")
            case 'Темна':
                customtkinter.set_appearance_mode("Dark")
            case 'Системна':
                customtkinter.set_appearance_mode("System")


    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def to_authorization(self):
        self.content_frame.destroy()
        self.navbar_frame.grid_remove()
        self.sidebar_frame.grid_remove()
        self.content_frame = Login(self, self, fg_color=("#FFFFFF", "#000000"))
        self.content_frame.grid(row=1, column=1, sticky='nsew', rowspan=4)

    def to_enter_data(self):
        self.content_frame.destroy()
        self.navbar_frame.configure()
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.navbar_frame.grid(row=0, column=1, sticky="nsew", rowspan=1)
        self.content_frame = EnterData(self, fg_color=("#FFFFFF", "#000000"))
        self.navbar_add_row_button.configure(command=lambda: TableOperations.add_empty_row(self.content_frame))
        self.content_frame.grid(row=1, column=1, sticky='nsew', rowspan=4)
        self.navbar_frame.grid(row=0, column=1, rowspan=1, sticky="new")

    def to_registration(self):
        self.content_frame.destroy()
        self.navbar_frame.grid_remove()
        self.sidebar_frame.grid_remove()
        self.content_frame = Register(self, self, fg_color=("#FFFFFF", "#000000"))
        self.content_frame.grid(row=1, column=1, sticky='nsew', rowspan=4)

    def to_teacher_load(self):
        from Views.TeacherLoad.TeacherLoadView import TeacherLoadView
        self.content_frame.destroy()
        self.content_frame = TeacherLoadView(self, fg_color=("#F5F5F5", "#000000"))
        self.content_frame.grid(row=1, column=1, sticky='nsew', rowspan=4)
        print("Successful switch to teacher load view")


if __name__ == "__main__":
    app = App()
    app.mainloop()
