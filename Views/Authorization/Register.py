import customtkinter as ctk
from Utils.dbconnect import DBConnect
from Classes.User_accounting.User import User


class Register(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.app = app
        self.grid_rowconfigure(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25), weight=1)

        self.login_label = ctk.CTkLabel(self, text="Реєстрація", font=("Calibri Bold", 20),
                                        text_color=("#3a7ebf", "#1f538d"),
                                        corner_radius=45)
        self.login_label.grid(row=3, column=13, sticky='nsew')

        self.login_text_box = ctk.CTkEntry(self, placeholder_text="Введіть логін", font=("Calibri", 16),
                                           corner_radius=45)
        self.login_text_box.grid(row=6, column=12, sticky='nsew', columnspan=3)

        self.password_text_box = ctk.CTkEntry(self, placeholder_text="Введіть пароль", font=("Calibri", 16),
                                              corner_radius=45, show="•")
        self.password_text_box.grid(row=9, column=12, sticky="nsew", columnspan=3)

        self.password_text_box2 = ctk.CTkEntry(self, placeholder_text="Введіть пароль ще раз", font=("Calibri", 16),
                                              corner_radius=45, show="•")
        self.password_text_box2.grid(row=12, column=12, sticky="nsew", columnspan=3)

        self.register_button = ctk.CTkButton(self, text="Зарєєструватись", corner_radius=30, font=('Calibri', 16), command=self.register_button_action)
        self.register_button.grid(row=14, column=13, sticky="nsew")

        self.change_form_label = ctk.CTkLabel(self, text="Уже маєте акаунт? Увійдіть в нього!", font=('Calibri', 16))
        self.change_form_label.bind("<Button-1>", lambda e: self.app.to_authorization())
        self.change_form_label.grid(row=16, column=13, sticky="nsew")

    def register_button_action(self):

        important_text_boxes = [self.login_text_box, self.password_text_box, self.password_text_box2]
        for text_box in important_text_boxes:
            if len(text_box.get()) == 0:
                print("Одне з полів не заповнено")
                return
        if self.password_text_box.get() != self.password_text_box2.get():
            print("Паролі не сходяться")
            return

        username = self.login_text_box.get()
        password = self.password_text_box.get()
        db = DBConnect()
        data = db.execute_query("SELECT username FROM accounts;")
        usernames = [username[0] for username in data]

        for existing_username in usernames:
            if username == existing_username:
                print("Користувач з таким ім'ям уже існує")
                return

        sql_query = f'''
                    INSERT INTO accounts(username, password) VALUES("{username}","{password}");
                '''
        db.execute_query(sql_query)
        print("Succesful")
        self.app.to_authorization()
