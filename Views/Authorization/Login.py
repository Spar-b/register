import customtkinter as ctk
from Utils.dbconnect import DBConnect
from Classes.User_accounting.User import User
import Utils.stats as stats


class Login(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_rowconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25), weight=1)

        self.app = app
        self.login_label = ctk.CTkLabel(self, text="Вхід в акаунт", font=("Calibri Bold", 20), text_color=("#3a7ebf", "#1f538d"),
                               corner_radius=30)
        self.login_label.grid(row=3, column=13, sticky='nsew')

        self.login_text_box = ctk.CTkEntry(self, placeholder_text="Введіть логін", font=("Calibri", 16), corner_radius=45)
        self.login_text_box.grid(row=6, column=12, sticky='nsew', columnspan=3)

        self.password_text_box = ctk.CTkEntry(self, placeholder_text="Введіть пароль", font=("Calibri", 16),
                                          corner_radius=30, show="•")
        self.password_text_box.grid(row=9, column=12, sticky="nsew", columnspan=3)

        self.login_button = ctk.CTkButton(self, text="Увійти", corner_radius=45, font=('Calibri', 16), command=self.login_button_action)
        self.login_button.grid(row=11, column=13, sticky="nsew")

        self.change_form_label = ctk.CTkLabel(self, text="Не маєте акаунту? Зарєєструйтесь!", font=('Calibri', 16))
        self.change_form_label.bind("<Button-1>", lambda e: app.to_registration())
        self.change_form_label.grid(row=13, column=13, sticky="nsew")

    def login_button_action(self):
        important_text_boxes = [self.login_text_box, self.password_text_box]
        for text_box in important_text_boxes:
            if len(text_box.get()) == 0:
                print("Одне з полів не заповнено")
                return

        username = self.login_text_box.get()
        password = self.password_text_box.get()

        db = DBConnect()
        data = db.execute_query("SELECT * FROM accounts;")
        ids = [id[0] for id in data]
        usernames = [username[1] for username in data]
        passwords = [password[2] for password in data]

        i = 0
        print(len(usernames))
        while i < len(usernames):
            if username == usernames[i] and password == passwords[i]:
                stats.current_user = User(ids[i], usernames[i], passwords[i])
                print(f"Succesful login to {username}")
                stats.current_parent_id = ids[i]
                self.app.to_enter_data()
            i += 1
