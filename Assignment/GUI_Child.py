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
import Driver_Races
import matplotlib.pyplot as plt
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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

        self.connections=None
        self.driver_name=None
    def set_selected_driver(self, driver_name, connection):
        self.connections = connection
        self.driver_name = driver_name
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

        self.races_btn = tk.Button(parent, text="Races", command=self.loadRaces,font=self.ComicF2)
        self.races_btn.grid(row=1, column=0, sticky=N + S + E + W, padx=5, pady=5)

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

    def loadRaces(self):
        # Get the drivers five fastest laps
        fastestsTimes =Driver_Races.get_driver_fastests_laps(self.connections, self.driver_name)

        fig, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2, 2, figsize=(8, 4), dpi=70)


        ax1.bar(fastestsTimes['racetracks'], fastestsTimes['fastestLapTime'])
        ax1.set_ylabel('Fastests Lap times')
        ax1.set_title('Top Five Fastest Lap Times')
        ax1.set_ylim(min(fastestsTimes['fastestLapTime']) - 0.5, max(fastestsTimes['fastestLapTime'] + 0.5 ))
        ax1.tick_params(axis='x', labelrotation=15)

        for patch in ax1.patches:
            x0, y0 = patch.get_xy()
            x0 += patch.get_width() / 2
            y0 += patch.get_height()
            color = patch.get_facecolor()
            ax1.text(x0, y0, str(y0), ha="center", va="bottom", color="white", clip_on=True, bbox=dict(ec="black",fc=color))

        # Get the drivers total wins and loses
        driver_wins,driver_loses = Driver_Races.get_driver_wins_losses(self.connections, self.driver_name)
        labels = 'Wins', 'Loses'

        ax2.pie((driver_wins,driver_loses), labels=labels, autopct='% 1.1f %%'
                ,shadow=True, startangle=90)
        ax2.axis('equal')
        ax2.set_title('Total Wins and Loses')


        # Get the drivers average pitstop time
        Driver_Races.get_driver_average_pitstop_lap(self.connections, self.driver_name)
        ax3.bar(fastestsTimes['racetracks'], fastestsTimes['fastestLapTime'])
        ax3.set_xlabel('Circuits')
        ax3.set_ylabel('Fastests Lap times')
        ax3.set_title('Top Five Fastest Lap Times')

        ax4.bar(fastestsTimes['racetracks'], fastestsTimes['fastestLapTime'])
        ax4.set_xlabel('Circuits')
        ax4.set_ylabel('Fastests Lap times')
        ax4.set_title('Top Five Fastest Lap Times')

        canvas = FigureCanvasTkAgg(fig, master=self.canvasPanel)
        canvas_widget = canvas.get_tk_widget()

        canvas_widget.grid(row=3,column=0,sticky=N+S+E+W)

        canvas.draw()

        # plt.bar(circuits, fastestsTimes, color = 'blue', width = 0.5)
        #
        # plt.xlabel("Fastest Lap Time")
        # plt.ylabel("Circuit names and countries")
        # plt.title("Top 5 Circuits with the fastest lap times")
        # plt.show()

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
