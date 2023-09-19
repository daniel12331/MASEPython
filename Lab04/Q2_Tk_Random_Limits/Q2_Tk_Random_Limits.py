import random
import tkinter as tk
import tkinter.messagebox
from tkinter import *

root = tk.Tk()
root.title("TUS midlands")
randVar = IntVar()
lowerStringVar = StringVar()
upperStringVar = StringVar()


def display_value_error(value):
    tkinter.messagebox.showwarning("Enter a valid limit", "The value: " + value + "\n is not valid, please enter a "
                                                                                  "valid int value")


def display_inversion_value_error(lower, upper):
    tkinter.messagebox.showinfo("Enter a valid limit", "The lower limit: " + str(lower) + " is greater then the upper "
                                                                                     "limit: " + str(upper))


def generate_random():
    if lowerStringVar.get() == '':
        lowerStringVar.set("0")

    else:
        try:
            lowerIntVar = int(lowerStringVar.get())

        except ValueError:
            display_value_error(lowerStringVar.get())

        try:
            upperIntVar = int(upperStringVar.get())

            if lowerIntVar < upperIntVar:
                randVar.set(random.randint(lowerIntVar, upperIntVar))
            else:
                display_inversion_value_error(lowerStringVar.get(), upperIntVar)
        except ValueError:
            display_value_error(upperStringVar.get())




def close_app():
    exit()


def main():
    l1 = tk.Label(root, text="Random Number Generator")
    l1.grid(row=0, column=0, columnspan=2)

    l2 = tk.Label(root, text="Randon Number")
    l2.grid(row=1, column=0)

    e1 = tk.Entry(root, textvariable=randVar)
    e1.grid(row=1, column=1)
    e1.configure(state="disabled")

    l2 = tk.Label(root, text="Lower Range")
    l2.grid(row=2, column=0)

    e2 = tk.Entry(root, textvariable=lowerStringVar)
    e2.grid(row=2, column=1)

    l2 = tk.Label(root, text="Upper Range")
    l2.grid(row=3, column=0)

    e3 = tk.Entry(root, textvariable=upperStringVar)
    e3.grid(row=3, column=1)

    b1 = tk.Button(root, text="Generate new", command=generate_random, font=("Calibri", 16))
    b1.grid(row=4, column=0)

    b2 = tk.Button(root, text="Close App", command=close_app, font=("Calibri", 16))
    b2.grid(row=4, column=1, sticky=tk.N + tk.S + tk.E + tk.W)

    root.mainloop()


if __name__ == '__main__':
    main()
