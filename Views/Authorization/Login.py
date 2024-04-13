import customtkinter
class Login(customtkinter.CTkFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8), weight=1)

        self.login_label = customtkinter.CTkLabel(self, text='Вхід в акаунт')
        self.login_label.grid(row=1, column=4, sticky='nsew')
