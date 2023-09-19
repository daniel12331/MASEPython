import tkinter as tk
from tkinter import font
from tkinter.ttk import Combobox
from tkinter import filedialog
import tkinter.messagebox
import tkinter.simpledialog
from tkinter import *


class AppGUI(tk.Tk):
    def __init__(self, master, title):
        self.master = master
        self.master.title(title)
        self.ComicF1 = font.Font(family="Comic Sans MS", size=16, weight="normal")
        self.ComicF2 = font.Font(family="Comic Sans MS", size=10, weight="normal")
        self.ComicF3 = font.Font(family="Comic Sans MS", size=12, weight="normal")

        self.firstNameString = StringVar()
        self.lastNameString = StringVar()

        self.contactMe = StringVar()
        self.contactMe.set("Enabled")

        self.emailAddress = StringVar()

        options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        self.ratingOption = IntVar()
        self.ratingOption.set(1)
        # Textvariables for the values specified by the user

        tk.Label(master, text="Basic Contact Registration", font=self.ComicF1).grid(row=0, column=0, columnspan=3,
                                                                                    sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Label(master, text="First Name", font=self.ComicF3).grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        tk.Entry(master, textvariable=self.firstNameString, font=self.ComicF3).grid(row=1, column=1, columnspan=2,
                                                                                    sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Label(master, text="Last Name", font=self.ComicF3).grid(row=2, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        tk.Entry(master, textvariable=self.lastNameString, font=self.ComicF3).grid(row=2, column=1, columnspan=2,
                                                                                   sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Radiobutton(master, text="Contact Me", command=self.contact_function, variable=self.contactMe,
                       value="Enabled", font=self.ComicF3).grid(row=3, column=0,
                                                                sticky=tk.N + tk.S + tk.E + tk.W)
        tk.Radiobutton(master, text="Don't Contact Me", command=self.contact_function, variable=self.contactMe,
                       value="Disabled", font=self.ComicF3).grid(row=3, column=2,
                                                                 sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Label(master, text="Email", font=self.ComicF3).grid(row=4, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.EmailEntry = tk.Entry(master, state=tk.NORMAL, textvariable=self.emailAddress, font=self.ComicF3)
        self.EmailEntry.grid(row=4, column=1, columnspan=2, sticky=tk.N + tk.S + tk.E + tk.W)

        tk.Label(master, text="Rating", font=self.ComicF3).grid(row=5, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        tk.OptionMenu(master, self.ratingOption, *options).grid(row=5, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

        self.register_button = tk.Button(master, text="Register",command=self.register, font=self.ComicF3).grid(row=6, column=0, columnspan=4,
                                                                                          sticky=tk.N + tk.S + tk.E + tk.W)

        self.TextArea = tk.Text(master, width=60, height=20)
        self.TextArea.grid(row=7, column=0, columnspan=4)
        self.TextArea.insert("1.0", self.readTextFile())

        self.close_button = tk.Button(master, text="Close", command=self.CloseApplication, font=self.ComicF3).grid(
            row=17, column=0, columnspan=4, sticky=tk.N + tk.S + tk.E + tk.W)

    def register(self):
        name = self.firstNameString.get() + " " + self.lastNameString.get()
        userRating = self.ratingOption.get()
        contactInfo = self.contactMe.get()

        if contactInfo == "Enabled":
            email = self.emailAddress.get()
            contactMsg = "Add: " + email
        else:
            contactMsg = "Contact not to be included"

        addMsg = "\nName: " + name + "\n" + contactMsg + "\nUser rating: " + str(userRating)
        self.insert(addMsg)

    def insert(self, msg):
        self.TextArea.insert(END, msg)


    def readTextFile(self):
        with open("HelloMsg.txt", "r") as file:
            data = file.read()
        return data


    def contact_function(self):
        if self.contactMe.get() == "Enabled":
            self.EmailEntry['state'] = tk.NORMAL
        else:
            self.EmailEntry['state'] = tk.DISABLED

    def CloseApplication(self):
        print('closing')
        self.master.destroy()
