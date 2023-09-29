
import tkinter as tk
from tkinter import font
from tkinter.ttk import Combobox
from tkinter import filedialog
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *

import mysql.connector
import pandas as pd

from PIL import ImageTk, Image


# from ABFrame_Obj import ABFrame
# from M29_Frame_Obj import M29Frame
# from WhirlPool_Frame_Obj import WhirlPoolFrame

class AppGUI(tk.Frame, ):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("Daniel Marko - Data Analytics")
        self.master.geometry("450x500")
        # This section creates the plot frame
        # self.ChildAB_Obj = ABFrame(self)
        # self.ChildAB_Obj.withdraw()
        # self.ChildM29_Obj = M29Frame(self)
        # self.ChildM29_Obj.withdraw()
        # self.ChildWhirl_Obj = WhirlPoolFrame(self)
        # self.ChildWhirl_Obj.withdraw()


        self.font_1 = font.Font(family="Calibri", size=16, weight="normal")
        self.font_2 = font.Font(family="Calibri", size=12, weight="normal")
        # Textvariables for the values specified by the user


        self.l1 = tk.Label(master, text="Daniel Marko - Data Analytics", font=self.font_1).grid(row=0,column=1,columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)


        self.img_airbnb = ImageTk.PhotoImage(Image.open("images/anayltics.jpg").resize((400,205)))
        self.label = Label(master, image = self.img_airbnb)
        self.label.grid(row=1,column=1,columnspan=2, ipadx=10, ipady=10, padx=10, pady=10)

        self.label_search = tk.Label(master, text="Search for F1 driver name : ").grid(row=2, column=1, columnspan=2,ipadx=10, ipady=0, padx=100, pady=0,sticky=tk.N + tk.S + tk.E + tk.W)

        self.ss = tk.Listbox(master)

        self.driver_name = StringVar()
        self.entry_name = tk.Entry(master, textvariable=self.driver_name).grid(row=3, column=1, columnspan=2,ipadx=10, ipady=5, padx=100, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
        self.search_btn = tk.Button(master, text="Search", command=self.search_query).grid(row=4, column=1, columnspan=2,ipadx=10, ipady=5, padx=100, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)


        self.close_button = tk.Button(master, text="Close", command=self.CloseApplication, font=self.font_2, ).grid(row=6,column=1,columnspan=2,ipadx=5, ipady=5, padx=10, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)

    def search_query(self):
        print(self.driver_name.get())
        if self.driver_name.get() == '':
            tkinter.messagebox.showwarning("No entry entered", "No Entry Entered, please enter a name")
        else:
            # Variables to connect to F1 DB
            F1_server = 'relational.fit.cvut.cz'
            F1_user = 'guest'
            F1_password = 'relational'
            F1_database = 'ErgastF1'
            # Connection to DB
            connection = mysql.connector.connect(
                host=F1_server,
                database=F1_database,
                user=F1_user,
                password=F1_password)
            # Query the names for analysis
            query_drivers_names = "SELECT concat(forename,' ', surname) as 'Drivers Names' FROM drivers where forename like '%{0}%'".format(self.driver_name.get())
            df_mysql = pd.read_sql(query_drivers_names, con=connection)
            values = df_mysql['Drivers Names']

            print(df_mysql)

    def showChildA(self):
        self.ChildAB_Obj.show()
        self.master.withdraw()

    def showChildM29(self):
        self.ChildM29_Obj.show()
        self.master.withdraw()

    def showChildWhirl(self):
        self.ChildWhirl_Obj.show()
        self.master.withdraw()


    def CloseApplication(self):
        print('closing')
        self.master.destroy()

    def show(self):
        """"""
        self.master.update()
        self.master.deiconify()