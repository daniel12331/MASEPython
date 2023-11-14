import pandas as pd
from tkinter import *
from GUI_main import AppGUI



F1_server = 'localhost'
F1_port = '3306'
F1_user = 'root'
F1_password = 'root'
F1_database = 'f1'

db_info=(F1_server, F1_port, F1_user,F1_password,F1_database)
def main():
    root = Tk()

    myGUI = AppGUI(root)
    root.title = "Daniel Marko"
    p1 = PhotoImage(file='images/f1_logo.png')
    root.iconphoto(False, p1)
    root.resizable(False, False)
    root.mainloop()


if __name__ == '__main__':
    main()