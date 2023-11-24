from tkinter import *
import tkinter as tk
from tkinter import font, ttk
import Driver_Profile
class Driver_Regression(tk.Toplevel):
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

        # MAC 13.3 RES
        # self.width = 1400
        # self.height = 800
        # self.geometry('1440x800')

        self.connections = None
        self.driver_name = None

        self.s_var = tk.StringVar()
        # self.s_var.trace_add('write', self.on)

    def set_selected_driver(self, driver_name, connection):
        self.connections = connection
        self.driver_name = driver_name
        self.title(driver_name)
        driver_info = Driver_Profile.get_driver_url(driver_name, connection)

        # Buttons section
        self.buttonPanel = tk.Frame(self, background="black")
        self.buttonPanel.pack(side="left", fill="y")
        self._layoutButtons(self.buttonPanel, driver_info)
        self.hide()


    def _layoutButtons(self, parent, driver_info):
        self.titleLabel = tk.Label(parent, text="Analyse", font=self.ComicF1)
        self.titleLabel.grid(row=0, column=0, sticky=N + S + E + W)

        self.close_Frame = tk.Button(parent, text="Go Back", command=self.hide, font=self.ComicF2)
        self.close_Frame.grid(row=6, column=0, sticky=N + S + E + W, padx=5, pady=5)

    def show(self):
        self.update()  # Update the window
        self.deiconify()  # Displays the window, after using either the iconify or the withdraw methods.

    def OverrideWindow(self):
        self.hide()  # Hide the window

    def hide(self):
        self.s_var.set("close")
        self.withdraw()