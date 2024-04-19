import tkinter
import tkinter.messagebox
import customtkinter
import CTkTable
from Views.enterdata import EnterData
from Views.Authorization.Login import Login
from Views.Authorization.Register import Register

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
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
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
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
        self.navbar_frame.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15), weight=1)

        self.navbar_add_row_button = customtkinter.CTkButton(self.navbar_frame, text="Додати рядок", command=self.content_frame.add_empty_row)
        self.navbar_add_row_button.grid(row=1, column=1, sticky="nsew")
        self.navbar_save_button = customtkinter.CTkButton(self.navbar_frame, text="Зберегти", font=customtkinter.CTkFont("Arial", 16), command=self.content_frame.save)
        self.navbar_save_button.grid(row=2, column=1, sticky="nsew")
        self.navbar_edit_button = customtkinter.CTkButton(self.navbar_frame, text="Редагування",
                                                          command=EnterData.switch_to_edit)
        self.navbar_edit_button.grid(row=1, column=2, sticky="nsew")

        self.navbar_edit_button = customtkinter.CTkButton(self.navbar_frame, text="Перехід",
                                                          command=EnterData.switch_to_open)
        self.navbar_edit_button.grid(row=2, column=2, sticky="nsew")

        self.to_authorization()

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):

        if new_appearance_mode == "Світла":
            customtkinter.set_appearance_mode("Light")
        if new_appearance_mode == "Темна":
            customtkinter.set_appearance_mode("Dark")
        if new_appearance_mode == "Системна":
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
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.navbar_frame.grid(row=0, column=1, sticky="nsew", rowspan=1)
        self.content_frame = EnterData(self, fg_color=("#FFFFFF", "#000000"))
        self.navbar_add_row_button.configure(command=self.content_frame.add_empty_row)
        self.content_frame.grid(row=1, column=1, sticky='nsew', rowspan=4)
        self.navbar_frame.grid(row=0, column=1, rowspan=1, sticky="new")

    def to_registration(self):
        self.content_frame.destroy()
        self.navbar_frame.grid_remove()
        self.sidebar_frame.grid_remove()
        self.content_frame = Register(self, self, fg_color=("#FFFFFF", "#000000"))
        self.content_frame.grid(row=1, column=1, sticky='nsew', rowspan=4)

if __name__ == "__main__":
    app = App()
    app.mainloop()
