import pandas as pd
from tkinter import *
from GUI_main import AppGUI



F1_server = 'relational.fit.cvut.cz'
F1_port = '3306'
F1_user = 'guest'
F1_password = 'relational'
F1_database = 'ErgastF1'


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