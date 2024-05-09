import customtkinter as ctk
from Utils.dbconnect import DBConnect
from Classes.User_accounting.User import User
import PIL.Image
import PIL.ImageTk


class Register(ctk.CTkFrame):
    def __init__(self, app, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.app = app
        self.grid_rowconfigure(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25), weight=1)
        self.grid_columnconfigure((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 22, 23, 24, 25), weight=1)

        self.password_char_active = True

        self.login_label = ctk.CTkLabel(self, text="Реєстрація", font=("Calibri Bold", 20),
                                        text_color=("#3a7ebf", "#1f538d"),
                                        corner_radius=45)
        self.login_label.grid(row=3, column=14, sticky='nsew')

        self.login_text_box = ctk.CTkEntry(self, placeholder_text="Введіть логін", font=("Calibri", 16),
                                           corner_radius=45, height=45)
        self.login_text_box.grid(row=6, column=13, sticky='ew', columnspan=3)

        self.view_image = PIL.Image.open(".././Images/Show-Hide-Password/view.png")
        self.hide_image = PIL.Image.open(".././Images/Show-Hide-Password/hide.png")

        self.show_password_image = ctk.CTkImage(light_image=self.view_image,
                                                          dark_image=self.view_image,
                                                          size=(45, 45))

        self.show_password_button = ctk.CTkButton(self, image=self.show_password_image, text="", fg_color="transparent",
                                                  command=self.switch_password_char)
        self.show_password_button.grid(row=8, column=16)

        self.password_text_box = ctk.CTkEntry(self, placeholder_text="Введіть пароль", font=("Calibri", 16),
                                              corner_radius=45, show="•", height=45)
        self.password_text_box.grid(row=8, column=13, sticky="ew", columnspan=3)

        self.password_text_box2 = ctk.CTkEntry(self, placeholder_text="Введіть пароль ще раз", font=("Calibri", 16),
                                              corner_radius=45, show="•", height=45)
        self.password_text_box2.grid(row=10, column=13, sticky="ew", columnspan=3)

        self.issue_text = ctk.CTkLabel(self, text="", text_color="#FF0000")
        self.issue_text.grid(row=11, column=14, sticky="nsew")

        self.register_button = ctk.CTkButton(self, text="Зарєєструватись", corner_radius=30, font=('Calibri', 16), command=self.register_button_action)
        self.register_button.grid(row=12, column=14, sticky="nsew")

        self.change_form_label = ctk.CTkLabel(self, text="Уже маєте акаунт? Увійдіть в нього!", font=('Calibri', 16))
        self.change_form_label.bind("<Button-1>", lambda e: self.app.to_authorization())
        self.change_form_label.grid(row=14, column=14, sticky="nsew")

    def register_button_action(self):

        important_text_boxes = [self.login_text_box, self.password_text_box, self.password_text_box2]
        for text_box in important_text_boxes:
            if len(text_box.get()) == 0:
                issue_string = "Одне з полів не заповнено"
                print(issue_string)
                self.issue_text.configure(text=issue_string)
                return
        if self.password_text_box.get() != self.password_text_box2.get():
            issue_string = "Паролі не сходяться"
            print(issue_string)
            self.issue_text.configure(text=issue_string)
            return

        username = self.login_text_box.get()
        password = self.password_text_box.get()
        db = DBConnect()
        data = db.execute_query("SELECT username FROM accounts;")
        usernames = [username[0] for username in data]

        for existing_username in usernames:
            if username == existing_username:
                issue_string = "Користувач з таким ім'ям уже існує"
                print(issue_string)
                self.issue_text.configure(text=issue_string)
                return

        sql_query = f'''
                    INSERT INTO accounts(username, password) VALUES("{username}","{password}");
                '''
        db.execute_query(sql_query)
        print("Succesful")
        self.app.to_authorization()

    def switch_password_char(self):
        if self.password_char_active:
            self.show_password_image.configure(light_image=self.hide_image, dark_image=self.hide_image)
            self.password_text_box.configure(show="")
            self.password_text_box2.configure(show="")
        else:
            self.show_password_image.configure(light_image=self.view_image, dark_image=self.view_image)
            self.password_text_box.configure(show="•")
            self.password_text_box2.configure(show="•")
        self.password_char_active = not self.password_char_active
