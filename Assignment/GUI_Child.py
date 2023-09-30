from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font
import webbrowser

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

        # Create two panels, one is for the buttons and the other is for the canvas (images)
        buttonPanel = tk.Frame(self, background="black")
        canvasPanel = tk.Frame(self, background="black")
        # Set the positioning of the panels
        buttonPanel.pack(side="left", fill="y")
        canvasPanel.pack(side="right", fill="both", expand=True)

        # ill in these two areas:
        self._layoutButtons(buttonPanel)
        self._layoutCanvas(canvasPanel)
        self.resizable(False, False)

    def set_selected_driver(self, driver_name):
        self.title(driver_name)

    def _layoutButtons(self, parent):
        self.titleLabel = tk.Label(parent, text="Analyse", font=self.ComicF1)
        self.titleLabel.grid(row=0, column=0, sticky=N+S+E+W)

        self.web_link = tk.Button(parent, text="Info", command=lambda url="https://www.astrobin.com/v0ov52/?nc=all": self.open_link(url), font=self.ComicF2)
        self.web_link.grid(row=1, column=0, sticky=N+S+E+W, padx=5, pady=5)

        self.video_link = tk.Button(parent, text="Buy Print", command=lambda url="https://cathrinmachin.myshopify.com/collections/cosmic-union-project/products/abel-85-30x40-canvas-layout": self.open_link(url), font=self.ComicF2)
        self.video_link.grid(row=2, column=0, sticky=N+S+E+W, padx=5, pady=5)

        self.close_Frame = tk.Button(parent, text="Close", command=self.hide, font=self.ComicF2)
        self.close_Frame.grid(row=3, column=0, sticky=N+S+E+W, padx=5, pady=5)


    def open_link(self,url):
        webbrowser.open(url)


    def _layoutCanvas(self, parent):
        img_Path = 'images/counties.jpg'
        self.image = ImageTk.PhotoImage(file = img_Path)
        width = self.image.width()
        height = self.image.height()
        self.canvas = tk.Canvas(parent, height=height, width=width)
        self.canvas.grid(row=3, column=0, sticky=N + S + E + W)
        self.canvas.create_image(0, 1, anchor='nw', image=self.image)

    def show(self):
        self.update()       # Update the window
        self.deiconify() #Displays the window, after using either the iconify or the withdraw methods.

    def OverrideWindow(self):
        self.hide() # Hide the window

    def hide(self):
        self.withdraw() #Removes the window from the screen, without destroying it.
        self.root.show()
