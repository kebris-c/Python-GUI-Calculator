#!/usr/bin/env python3

import tkinter as tk
from Calculator import Calc

if __name__ == '__main__':
    root = tk.Tk() # Main Window
    gui = Calc(root)

    root.geometry("280x230")
    root.resizable(False, False)

    root.mainloop()
