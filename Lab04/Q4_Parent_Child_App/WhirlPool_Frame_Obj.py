import tkinter.messagebox
from tkinter import *
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import font
import webbrowser
import requests
import os


def display_msg(error_code, msg):
    if error_code == 0:
        tkinter.messagebox.showinfo("Image Saved Successfully", msg)
    else:
        tkinter.messagebox.showerror("Image Error", msg)


class WhirlPoolFrame(tk.Toplevel):

    def __init__(self, master):
        tk.Toplevel.__init__(self, master)  # Initialize superclass
        """Constructor"""
        self.root = master
        # Title for window and do not kill the window
        self.title("Child WhirlPool Frame")
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

    def open_link(self, url):
        webbrowser.open(url)

    def download_img(self, img_url):

        try:
            data = requests.get(img_url).content
            f = open('whirlpool.jpg', 'wb')
            f.write(data)
            f.close()

            img = Image.open("whirlpool.jpg")
            img_name = f.name
            wid, hgt = img.size

            img_format = img.format

            msg = "Image Name: {0} \n Image Size: {1} * {2} \n Image Format: {3} \n Image saved to app folder \n Click ok to display image".format(img_name, wid, hgt, img_format)
            display_msg(0, msg)
        except:
            display_msg(1, "Error")

    def _layoutButtons(self, parent):
        self.titleLabel = tk.Label(parent, text="Child WhirlPool", font=self.ComicF1)
        self.titleLabel.grid(row=0, column=0, sticky=N + S + E + W)

        self.web_link = tk.Button(parent, text="Info", command=lambda
            url="https://www.esa.int/ESA_Multimedia/Images/2023/08/Webb_captures_a_cosmic_Whirlpool": self.open_link(
            url), font=self.ComicF2)
        self.web_link.grid(row=1, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.image_link = tk.Button(parent, text="Download High Res", command=lambda
            url="https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2023/08/webb_captures_a_cosmic_whirlpool/25056954-1-eng-GB/Webb_captures_a_cosmic_Whirlpool.jpg": self.download_img(
            url), font=self.ComicF2)
        self.image_link.grid(row=2, column=0, sticky=N + S + E + W, padx=5, pady=5)

        self.close_Frame = tk.Button(parent, text="Close", command=self.hide, font=self.ComicF2)
        self.close_Frame.grid(row=3, column=0, sticky=N + S + E + W, padx=5, pady=5)

    def _layoutCanvas(self, parent):
        img_Path = 'images/Whirlpool.jpg'
        self.image = ImageTk.PhotoImage(file=img_Path)
        width = self.image.width()
        height = self.image.height()
        self.canvas = tk.Canvas(parent, height=height, width=width)
        self.canvas.grid(row=3, column=0, sticky=N + S + E + W)
        self.canvas.create_image(0, 1, anchor='nw', image=self.image)

    def show(self):
        self.update()  # Update the window
        self.deiconify()  # Displays the window, after using either the iconify or the withdraw methods.

    def OverrideWindow(self):
        self.hide()  # Hide the window

    def hide(self):
        self.withdraw()  # Removes the window from the screen, without destroying it.
        self.root.show()
