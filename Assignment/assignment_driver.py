import pandas as pd
from tkinter import *
from GUI_main import AppGUI

def main():
    root = Tk()

    myGUI = AppGUI(root)
    root.title = "Daniel Marko"
    root.resizable(False, False)
    root.mainloop()

    # df = pd.read_csv('resources/listings.csv')
    # print(df.info())
    # print(df['neighbourhood_cleansed'].unique())


if __name__ == '__main__':
    main()