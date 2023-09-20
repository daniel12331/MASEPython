
import tkinter as tk
from tkinter import font
from tkinter.ttk import Combobox
from tkinter import filedialog
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *
from ABFrame_Obj import ABFrame
from M29_Frame_Obj import M29Frame
from WhirlPool_Frame_Obj import WhirlPoolFrame

class AppGUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        #self.master.title(aTitle)

        # This section creates the plot frame
        self.ChildAB_Obj = ABFrame(self)
        self.ChildAB_Obj.withdraw()
        self.ChildM29_Obj = M29Frame(self)
        self.ChildM29_Obj.withdraw()
        self.ChildWhirl_Obj = WhirlPoolFrame(self)
        self.ChildWhirl_Obj.withdraw()


        self.font_1 = font.Font(family="Calibri", size=16, weight="normal")
        self.font_2 = font.Font(family="Calibri", size=12, weight="normal")

        # Textvariables for the values specified by the user

        self.l1 = tk.Label(master, text="Celestial Objects", font=self.font_1).grid(row=0,column=0,columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        self.childAB_Button = tk.Button(master, text="Abeil", command=self.showChildA, font=self.font_2)
        self.childAB_Button.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        self.childM29_Button = tk.Button(master, text="M29", command=self.showChildM29, font=self.font_2)
        self.childM29_Button.grid(row=1, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.childWhirl_Button = tk.Button(master, text="Whirlpool", command=self.showChildWhirl, font=self.font_2)
        self.childWhirl_Button.grid(row=2, column=0, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)


        self.close_button = tk.Button(master, text="Close", command=self.CloseApplication, font=self.font_2).grid(row=3,column=0,columnspan=2,sticky=tk.N + tk.S + tk.E + tk.W)

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