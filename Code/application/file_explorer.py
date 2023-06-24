import tkinter as tk
from tkinter import filedialog

def browse_files():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File")
    print(filename)
    return filename

def run():
    root = tk.Tk()

    root.title('File Explorer')
