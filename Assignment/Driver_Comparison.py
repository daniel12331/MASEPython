import tkinter.messagebox
from tkinter import *
import tkinter as tk
from tkinter import font
import pandas as pd
from PIL import ImageTk
import Driver_Profile
import Driver_Data_1


class Driver_Comparison(tk.Toplevel):
    def __init__(self, master):
        tk.Toplevel.__init__(self, master)  # Initialize superclass
        """Constructor"""
        self.root = master
        # Title for window and do not kill the window
        self.protocol('WM_DELETE_WINDOW', self.OverrideWindow)

        # Set up the fonts you want to use
        self.ComicF1 = font.Font(family="Calibri", size=16, weight="normal")
        self.ComicF2 = font.Font(family="Calibri", size=12, weight="normal")

        self.resizable(False, False)

        # Windows 1920x1080
        self.width = 1900
        self.height = 1080
        self.geometry('400x400')

        self.connections = None
        self.driver_name = None

        self.s_var = tk.StringVar()

    def set_selected_driver(self, driver_name, connection):
        self.connections = connection
        self.driver_name = driver_name
        self.title("Compare Driver")
        self.driver_id = Driver_Data_1.get_driver_id(driver_name, connection)

        # Buttons section
        self.buttonPanel = tk.Frame(self, background="black")
        self.buttonPanel.pack(fill="y")
        self._layoutButtons(self.buttonPanel)

    def _layoutButtons(self, parent):
        self.titleLabel = tk.Label(parent, text="Comparison Analysis", font='Helvetica 18 bold')
        self.titleLabel.grid(row=0, column=0, sticky=N + S + E + W)

        self.label_search = tk.Label(parent, text="Search for F1 driver name : ")
        self.label_search.grid(row=2, column=0,sticky=tk.N + tk.S + tk.E + tk.W)

        self.driver_name = StringVar()
        self.entry_name = tk.Entry(parent, textvariable=self.driver_name)
        self.entry_name.grid(row=3, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.search_btn = tk.Button(parent, text="Search", command=self.search_query)
        self.search_btn.grid(row=4, column=0,sticky=tk.N + tk.S + tk.E + tk.W)

        self.list_box = tk.Listbox(parent)
        self.list_box.grid(row=5, column=0,sticky=tk.N + tk.S + tk.E + tk.W)

        self.selected_driver_name = None

        self.childAB_Button = tk.Button(parent, text="Compare", command=self.analyse_btn)
        self.childAB_Button.grid(row=6, column=0,sticky=tk.N + tk.S + tk.E + tk.W)

    def search_query(self):
        if self.driver_name.get() == '':
            tkinter.messagebox.showwarning("No entry entered", "No Entry Entered, please enter a name")
        else:

            # Query the names for analysis
            query_drivers_names = "SELECT concat(forename,' ', surname) as 'Drivers Names' FROM drivers where forename like '%{0}%'".format(self.driver_name.get())
            df_mysql = pd.read_sql(query_drivers_names, con=self.connections)

            # clear the names in the list box prior to displaying the selection
            self.list_box.delete(0, tk.END)

            #
            if not df_mysql.empty:
                values = df_mysql['Drivers Names']
                for value in values:
                    self.list_box.insert(tk.END, value)
            else:
                tkinter.messagebox.showwarning("No Results", "No matching results found.")

    def analyse_btn(self):
        selected_index = self.list_box.curselection()
        if selected_index != ():
            self.selected_driver_name = self.list_box.get(selected_index)
            self.hide()
        else:
            tkinter.messagebox.showwarning("No driver selected", "No Driver selected!")

    def loadDriversData(self):
        driver_info = Driver_Profile.get_driver_url(self.selected_driver_name, self.connections)
        try:
            self.pil_image = Driver_Profile.get_driver_image(driver_info)

        except Exception as e:
            img_Path = 'images/no_image.png'
            self.pil_image = ImageTk.PhotoImage(file=img_Path)

        return self.pil_image, self.selected_driver_name

    def show(self):
        self.update()  # Update the window
        self.deiconify()  # Displays the window, after using either the iconify or the withdraw methods.

    def OverrideWindow(self):
        self.hide()  # Hide the window

    def hide(self):
        self.buttonPanel.destroy()
        self.s_var.set("close")
        self.withdraw()
