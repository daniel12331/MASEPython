import tkinter as tk
from tkinter import font
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *

import mysql.connector
import pandas as pd

from PIL import ImageTk, Image
from GUI_Child import AChild


class AppGUI(tk.Frame):

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title("Daniel Marko - Data Analytics")
        self.master.geometry("450x700")

        # Variables to connect to F1 DB
        self.connection = 'mysql+mysqlconnector://guest:relational@relational.fit.cvut.cz/ErgastF1'

        # This section creates the plot frame
        self.ChildA_Obj = AChild(self)
        self.ChildA_Obj.withdraw()


        self.font_1 = font.Font(family="Calibri", size=16, weight="normal")
        self.font_2 = font.Font(family="Calibri", size=12, weight="normal")


        self.l1 = tk.Label(master, text="Daniel Marko - Data Analytics", font=self.font_1).grid(row=0,column=1,columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)


        self.img_airbnb = ImageTk.PhotoImage(Image.open("images/f1_team.jpg").resize((400, 205)))
        self.label = Label(master, image = self.img_airbnb)
        self.label.grid(row=1,column=1,columnspan=2, ipadx=10, ipady=10, padx=10, pady=10)

        self.label_search = tk.Label(master, text="Search for F1 driver name : ").grid(row=2, column=1, columnspan=2,ipadx=10, ipady=0, padx=100, pady=0,sticky=tk.N + tk.S + tk.E + tk.W)


        self.driver_name = StringVar()
        self.entry_name = tk.Entry(master, textvariable=self.driver_name).grid(row=3, column=1, columnspan=2,ipadx=10, ipady=5, padx=100, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)
        self.search_btn = tk.Button(master, text="Search", command=self.search_query).grid(row=4, column=1, columnspan=2,ipadx=10, ipady=5, padx=100, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)

        self.list_box = tk.Listbox(master)
        self.list_box.grid(row=5, column=1, columnspan=2, ipadx=10, ipady=5, padx=100, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)

        self.selected_driver_name = None

        self.childAB_Button = tk.Button(master, text="Analyse", command=self.analyse_btn, font=self.font_2)
        self.childAB_Button.grid(row=6, column=1, columnspan=2, ipadx=10, ipady=5, padx=100, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)

        self.close_button = tk.Button(master, text="Close", command=self.CloseApplication, font=self.font_2, ).grid(row=7,column=1,columnspan=2,ipadx=5, ipady=5, padx=10, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)

    def analyse_btn(self):
        selected_index = self.list_box.curselection()
        if selected_index != ():
            selected_driver_name = self.list_box.get(selected_index)
            self.ChildA_Obj.set_selected_driver(selected_driver_name, self.connection)
            self.ChildA_Obj.show()
            self.master.withdraw()
        else:
            tkinter.messagebox.showwarning("No driver selected", "No Driver selected!")


    def search_query(self):
        if self.driver_name.get() == '':
            tkinter.messagebox.showwarning("No entry entered", "No Entry Entered, please enter a name")
        else:

            # Query the names for analysis
            query_drivers_names = "SELECT concat(forename,' ', surname) as 'Drivers Names' FROM drivers where forename like '%{0}%'".format(self.driver_name.get())
            df_mysql = pd.read_sql(query_drivers_names, con=self.connection)

            # clear the names in the list box prior to displaying the selection
            self.list_box.delete(0, tk.END)

            #
            if not df_mysql.empty:
                values = df_mysql['Drivers Names']
                for value in values:
                    self.list_box.insert(tk.END, value)
            else:
                tkinter.messagebox.showwarning("No Results", "No matching results found.")


    def CloseApplication(self):
        print('closing')
        self.master.destroy()

    def show(self):
        self.master.update()
        self.master.deiconify()