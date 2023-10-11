import io
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font
import webbrowser
import pandas as pd
import requests
from bs4 import BeautifulSoup
import Driver_Profile

class AChild(tk.Toplevel):
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
        self.geometry('1920x1080')

    def set_selected_driver(self, driver_name, connection):
        self.title(driver_name)
        driver_info = Driver_Profile.get_driver_url(driver_name, connection)

        # Buttons section
        self.buttonPanel = tk.Frame(self, background="black")
        self.buttonPanel.pack(side="left", fill="y")
        self._layoutButtons(self.buttonPanel, driver_info)

        # Canvas section
        self.canvasPanel = tk.Frame(self, background="black")
        self.canvasPanel.pack(side="right", fill="both", expand=True)
        self._layoutCanvas(self.canvasPanel, driver_info)


    def _layoutButtons(self, parent, driver_info):
        self.titleLabel = tk.Label(parent, text="Analyse", font=self.ComicF1)
        self.titleLabel.grid(row=0, column=0, sticky=N+S+E+W)

        self.web_link = tk.Button(parent, text="Info", command=lambda url=driver_info: self.open_link(url), font=self.ComicF2)
        self.web_link.grid(row=1, column=0, sticky=N+S+E+W, padx=5, pady=5)

        self.close_Frame = tk.Button(parent, text="Go Back", command=self.hide, font=self.ComicF2)
        self.close_Frame.grid(row=3, column=0, sticky=N + S + E + W, padx=5, pady=5)

    def open_link(self,url):
        webbrowser.open(url)

    def _layoutCanvas(self, parent, driver_info):

        try:
            pil_image = Driver_Profile.get_driver_image(driver_info)
            self.image = ImageTk.PhotoImage(pil_image)

            self.canvas = tk.Canvas(parent, height=1080, width=1920)
            self.canvas.grid(row=3, column=0, sticky=N + S + E + W)
            self.canvas.create_image(0, 1, anchor='nw', image=self.image)

        except Exception as e:
            self.loadDefaultImg(parent)

    def loadDefaultImg(self, parent):
        img_Path = 'images/no_image.png'
        self.image = ImageTk.PhotoImage(file=img_Path)

        self.canvas = tk.Canvas(parent, height=1080, width=1920)
        self.canvas.grid(row=3, column=0, sticky=N + S + E + W)
        self.canvas.create_image(0, 1, anchor='nw', image=self.image)

    def show(self):
        self.update()       # Update the window
        self.deiconify() #Displays the window, after using either the iconify or the withdraw methods.

    def OverrideWindow(self):
        self.hide() # Hide the window

    def hide(self):
        self.withdraw() #Removes the window from the screen, without destroying it.
        self.buttonPanel.destroy()
        self.canvasPanel.destroy()
        self.root.show()
