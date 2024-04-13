import customtkinter as ctk


class Register(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25), weight=1)
        self.grid_columnconfigure((1, 2, 3), weight=1)

        self.login_label = ctk.CTkLabel(self, text="Реєстрація", font=("Calibri Bold", 20),
                                        text_color=("#3a7ebf", "#1f538d"),
                                        corner_radius=45)
        self.login_label.grid(row=3, column=2, sticky='nsew')

        self.login_text_box = ctk.CTkEntry(self, placeholder_text="Введіть логін", font=("Calibri", 16),
                                           corner_radius=45)
        self.login_text_box.grid(row=6, column=2, sticky='nsew')

        self.password_text_box = ctk.CTkEntry(self, placeholder_text="Введіть пароль", font=("Calibri", 16),
                                              corner_radius=45, show="•")
        self.password_text_box.grid(row=9, column=2, sticky="nsew")

        self.password_text_box2 = ctk.CTkEntry(self, placeholder_text="Введіть пароль ще раз", font=("Calibri", 16),
                                              corner_radius=45, show="•")
        self.password_text_box2.grid(row=12, column=2, sticky="nsew")

        self.change_form_label = ctk.CTkLabel(self, text="Уже маєте акаунт? Увійдіть в нього!", font=('Calibri', 16))
        self.change_form_label.bind("<Button-1>", lambda e: app.to_authorization())
        self.change_form_label.grid(row=14, column=2, sticky="nsew")
