#!/usr/bin/env python3

import tkinter as tk

class   Calc:
    def __init__(self, master):
        self.master = master
        self.display = tk.Entry(master, width=15, font=("Arial", 23), bd=10, \
                insertwidth=1, bg="#6495DE", justify="right")
        self.display.grid(row=0, column=0, columnspan=4)
        self.curr = ""
        self.nums = []
        self.last_op = None
        self.last_val = None

        row = 1
        col = 0
        buttons = [
                "7", "8", "9", "/",
                "4", "5", "6", "*",
                "1", "2", "3", "-",
                "C", "0", ".", "+",
                "Esc", "⌫", "="
                ]
        for button in buttons:
            self.build_button(button, row, col)
            col += 1
            if col >= 4:
                col = 0
                row += 1

        self.master.bind("<Key>", self.key_press)

# ===================== KEYS =====================
    def key_press(self, event):
        key = event.char
        if key == "\r":
            self.calculate(key)
        elif key == "\x08":
            self.backspace(key)
        elif key == "\x1b":
            self.escape(key)
        elif self.isnum(key):
            self.press_num(key)
        elif self.isoperator(key):
            self.press_op(key)
        else:
            return

# ===================== CORE =====================
    def calculate(self, button):
        print(f"\n[+] You are pressed the button: <ENTER>")
        if self.curr and not self.nums and self.last_op and self.last_val:
            expression = f"{self.curr}{self.last_op}{self.last_val}"
        else:
            if self.curr:
                self.nums.append(self.curr)
                self.curr = ""
            if len(self.nums) < 3:
                return
            self.last_op = self.nums[-2]
            self.last_val = self.nums[-1]
            expression = "".join(self.nums)
        print(f"[+] Expression to calculate: {expression}")
        try:
            result = eval(expression)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display.delete(0, "end")
            self.display.insert("end", str(result))
            self.curr = str(result)
            self.nums = []
            print(f"[+] Result: {result}")
        except Exception as e:
            self.display.delete(0, "end")
            self.display.insert("end", "Error")
            self.curr = ""
            self.nums = []
            print(f"[!] Error: {e}")

    def press_op(self, button):
        if not self.curr and self.nums and self.nums[-1] in "+-*/":
            return
        self.last_op = None
        self.last_val = None
        if self.curr:
            self.nums.append(self.curr) # Append number
            self.curr = "" # Reset current number
        self.nums.append(button) # Append operator
        self.display.insert("end", button) # Display operator
        print(f"\n[+] You are pressed the button: {button}")
        print(f"[+] Current expression on buffer: {self.nums}")

    def press_num(self, button):
        self.display.insert("end", button) # Display num or '.'
        self.curr += button # Add to current number (e.g.: "2.3" + "4" -> "2.34")
        print(f"\n[+] You are pressed the button: {button}")
        print(f"[+] Current number = {self.curr}")

    def backspace(self, button):
        if not self.display.get():
            return
        self.display.delete(len(self.display.get()) - 1, "end") # Delete last char from display
        if self.curr: # If we are writing a number
            self.curr = self.curr[:-1]
        elif self.nums: # If there is not a current number we are writing nums[]
            last = self.nums.pop()
            if last not in "+-*/": # If it is a num, return to curr except last char
                self.curr = last[:-1]
                if self.curr: # If still remaining, reinsert it
                    self.nums.append(self.curr)
                    self.curr = ""
        print(f"\n[+] You are pressed the button: <BACKSPACE>")
        print(f"[+] Current number: {self.curr}")
        print(f"[+] Current expression on buffer: {self.nums}")

    def clear_display(self, button):
        print(f"\n[+] You are pressed the button: {button}")
        self.display.delete(0, "end")
        self.curr = ""
        self.nums = []
        self.last_op = None
        self.last_val = None

    def escape(self, button):
        print(f"\n[+] You are pressed the button: <ESC>")
        print(f"[+] Exit...")
        self.master.quit()

# ===================== UTILS =====================
    def isoperator(self, button):
        return button in "+-*/"

    def isnum(self, button):
        return button in "0123456789."

    def build_button(self, button, row, col):
        if button == "C":
            b = tk.Button(self.master, text=button, width=4, command=lambda: self.clear_display(button))
        elif button == "=":
            b = tk.Button(self.master, text=button, width=4, command=lambda: self.calculate(button))
        elif self.isoperator(button):
            b = tk.Button(self.master, text=button, width=4, command=lambda: self.press_op(button))
        elif self.isnum(button):
            b = tk.Button(self.master, text=button, width=4, command=lambda: self.press_num(button))
        elif button == "⌫":
            b = tk.Button(self.master, text=button, width=4, command=lambda: self.backspace(button))
        elif button == "Esc":
            b = tk.Button(self.master, text=button, width=4, command=lambda: self.escape(button))
        else:
            print(f"\n[!] You are pressed invalid button: {button}")
        b.grid(row=row, column=col)
