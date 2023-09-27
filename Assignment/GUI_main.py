
import tkinter as tk
from tkinter import font
from tkinter.ttk import Combobox
from tkinter import filedialog
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *

from PIL import ImageTk, Image


# from ABFrame_Obj import ABFrame
# from M29_Frame_Obj import M29Frame
# from WhirlPool_Frame_Obj import WhirlPoolFrame

class AppGUI(tk.Frame):
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



        self.img_airbnb = ImageTk.PhotoImage(Image.open("images/airbnb.png"))
        self.label = Label(master, image = self.img_airbnb)
        self.label.grid(row=1,column=1,columnspan=2, ipadx=10, ipady=10, padx=10, pady=10)

        self.childDun_Button = tk.Button(master, text="Dun Laoghaire-Rathdown", command=self.showChildA, font=self.font_2)
        self.childDun_Button.grid(row=2, column=1, columnspan=2,ipadx=5, ipady=5, padx=10, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.childCity_Button = tk.Button(master, text="Dublin City", command=self.showChildM29, font=self.font_2)
        self.childCity_Button.grid(row=3, column=1, columnspan=2, ipadx=5, ipady=5, padx=10, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.childSouth_Button = tk.Button(master, text="South Dublin", command=self.showChildWhirl, font=self.font_2)
        self.childSouth_Button.grid(row=4, column=1, columnspan=2, ipadx=5, ipady=5, padx=10, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

        self.childFingal_Button = tk.Button(master, text="Fingal", command=self.showChildWhirl, font=self.font_2)
        self.childFingal_Button.grid(row=5, column=1, columnspan=2, ipadx=5, ipady=5, padx=10, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)


        self.close_button = tk.Button(master, text="Close", command=self.CloseApplication, font=self.font_2, bg='red').grid(row=6,column=1,columnspan=2,ipadx=5, ipady=5, padx=10, pady=5,sticky=tk.N + tk.S + tk.E + tk.W)

    def _layoutCanvas(self, parent):
        img_Path = 'images/airbnb.png'
        self.image = ImageTk.PhotoImage(file=img_Path)
        width = self.image.width()
        height = self.image.height()
        self.canvas = tk.Canvas(parent, height=height, width=width)
        self.canvas.grid(row=3, column=0, sticky=N + S + E + W)
        self.canvas.create_image(0, 1, anchor='nw', image=self.image)

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