# main.py

from tkinter import Tk
from gui.main_window import MainWindow
from gui.login_page import LoginPage
from app_logging import logger

app = MainWindow

def on_login_success():
    global login_window
    login_window.destroy()  # Close the login window
    # app = MainWindow()
    app.mainloop()

def main():
    global login_window
    logger.info("""ℹ️ Application Start :
                ###################################################################################
                ##                             ULTRA-AIM-PRO                                     ##
                ##                                                                               ##
                ##  Ultra96-based  AI-Managed Performance and Reliability Optimization system    ##
                ##                                                                               ##
                ##                  Created by: Dark Bors v2.0.2-beta                            ##
                ##                                                                               ##
                ##                                                                 Final Project ##
                ###################################################################################
                """)  # Log that the application has started    # root = Tk()
    # app.withdraw()  # Optionally hide the root window
    login_window = LoginPage(login_callback=on_login_success)
    login_window.mainloop()

if __name__ == '__main__':
    main()