import tkinter as tk
import file_manager as fm
import os
from tkinter import messagebox

global root, entry_frame, button_frame, entry

def close():
    global root, entry_frame, button_frame, entry
    root.grab_release()
    root.destroy()

def save():
    global entry
    if ((os.path.isdir(entry.get())) and (entry.get() != '')):
        default_directory = entry.get()
        fm.save_default_directory(default_directory)
    else:
        messagebox.showerror('Error', 'Not a directory')

def run():
    global root, entry_frame, button_frame, entry
    root = tk.Toplevel()
    root.grab_set()

    root.title("Default Directory")
    root.rowconfigure(2, weight=1)
    root.columnconfigure(1, weight=1)

    entry_frame = tk.Frame(root)
    entry_frame.rowconfigure(0, weight=1)
    entry_frame.columnconfigure(0, weight=1)
    entry_frame.grid(row=0, column=0, sticky='nsew')

    button_frame = tk.Frame(root)
    button_frame.rowconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)
    button_frame.grid(row=1, column=0, sticky='nsew')

    entry = tk.Entry(entry_frame, font=("Arial", 10), width=48)
    entry.grid(row=0, column=0, pady=10, padx=10)
    entry.insert(0, fm.load_default_directory())
    tk.Button(button_frame, text="       Save        ", font=("Arial", 15), command=save).grid(row=0, column=0, padx=10, pady=10)
    tk.Button(button_frame, text="       Exit        ", font=("Arial", 15), command=close).grid(row=0, column=1, padx=10, pady=10)

    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()
    
