# login_page.py

from customtkinter import CTk, CTkLabel, CTkEntry, CTkButton
from app_logging import logger
from tkinter import messagebox  # to display the message box


class LoginPage(CTk):
    def __init__(self, parent=None, login_callback=None):
        super().__init__()
        self.login_callback = login_callback

        self.title("Login")
        self.geometry("400x200")

        self.username_label = CTkLabel(self, text="Username:")
        self.username_label.pack()

        self.username_entry = CTkEntry(self)
        self.username_entry.pack()

        self.password_label = CTkLabel(self, text="Password:")
        self.password_label.pack()

        self.password_entry = CTkEntry(self, show="*")
        self.password_entry.pack()

        self.login_button = CTkButton(self, text="Login", command=self.on_login_clicked)
        self.login_button.pack()

    # Inside LoginPage class
    def on_login_clicked(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "b" and password == "b":
            self.destroy()  # Close the login window
            self.open_main_window()  # Open the main window
        else:
            logger.info("Login Failed", "Incorrect username or password")
            # Display error message
            messagebox.showerror("Login Failed", "Incorrect username or password")

    def open_main_window(self):
        from gui.main_window import MainWindow  # Import here to avoid circular imports
        main_app = MainWindow()
        main_app.mainloop()