import random
import tkinter as tk
from tkinter import *
from tkinter import font

root = tk.Tk()
root.title("TUS midlands")
randVar = IntVar()


def generate_random():
    randVar.set(random.randint(1, 100))


def close_app():
    exit()


def main():
    generate_random()

    l1 = tk.Label(root, text="Random Number Generator")
    l1.grid(row=0, column=0, columnspan=2)

    l2 = tk.Label(root, text="Randon Number")
    l2.grid(row=1, column=0)

    e1 = tk.Entry(root, textvariable=randVar)
    e1.grid(row=1, column=1)
    e1.configure(state="disabled")

    b1 = tk.Button(root, text="Generate new", command=generate_random, font=("Calibri", 16))
    b1.grid(row=2, column=0)

    b2 = tk.Button(root, text="Close App", command=close_app, font=("Calibri", 16))
    b2.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    root.mainloop()


if __name__ == '__main__':
    main()
