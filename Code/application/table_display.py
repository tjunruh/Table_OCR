from tksheet import Sheet
import tkinter as tk

def run(predictions, columns):
    rows = int(len(predictions)/columns)
    root = tk.Tk()
    root.grid_columnconfigure(0, weight = 1)
    root.grid_rowconfigure(0, weight = 1)
    frame = tk.Frame(root)
    frame.grid_columnconfigure(0, weight = 1)
    frame.grid_rowconfigure(0, weight = 1)
    cells = [[predictions[c + (r * columns)] for c in range(columns)] for r in range(rows)]
    sheet = Sheet(frame, data=cells)
    sheet.enable_bindings()
    sheet.font(newfont = ("century Gothic", 9, "normal"))
    frame.grid(row=0, column=0, sticky="nsew")
    sheet.grid(row=0, column=0, sticky="nsew")

    root.mainloop()
