import pandas as pd
from tkinter import *
from GUI_main import AppGUI


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