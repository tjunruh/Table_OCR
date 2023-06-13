import tkinter as tk
from tkscrolledframe import ScrolledFrame

def delete_entry(entry1, entry2, button1):
    global rows, shorthand_list
    for e1, e2, b1 in shorthand_list:
        if e1 == entry1:
            e1.destroy()
            
        if e2 == entry2:
            e2.destroy()
            
        if b1 == button1:
            b1.destroy()

def create_entry():
    global rows, shorthand_list
    row = rows
    entry1=tk.Entry(edit_frame, font=("Arial", 10), width=24)
    entry2=tk.Entry(edit_frame, font=("Arial", 10), width=24)
    button1=tk.Button(edit_frame, text="  X  ", font=("Arial", 10), command=lambda :delete_entry(entry1, entry2, button1))
    shorthand_list.append([entry1, entry2, button1])
    shorthand_list[row][0].grid(row=rows, column=0, sticky='nsew')
    shorthand_list[row][1].grid(row=rows, column=1, sticky='nsew')
    shorthand_list[row][2].grid(row=rows, column=2, sticky='nsew')
    edit_frame.rowconfigure(rows, weight=1)
    rows += 1

root = tk.Tk()
rows = 0
shorthand_list = []
root.title("Edit Shorthand")
root.rowconfigure(3, weight=1)
root.columnconfigure(2, weight=1)

title_frame = tk.Frame(root)
title_frame.rowconfigure(0, weight=1)
title_frame.columnconfigure(1, weight=1)
title_frame.grid(row=0, column=0, sticky='nsew')

button_frame = tk.Frame(root)
button_frame.rowconfigure(0, weight=1)
button_frame.columnconfigure(0, weight=1)
button_frame.grid(row=2, column=0, sticky='nsew')

scroll_frame = ScrolledFrame(root)
scroll_frame.grid(row=1, column=0, sticky='nsew')
scroll_frame.bind_arrow_keys(root)
scroll_frame.bind_scroll_wheel(root)
edit_frame = scroll_frame.display_widget(tk.Frame)
edit_frame.rowconfigure(1, weight=1)
edit_frame.columnconfigure(3, weight=1)



tk.Label(title_frame, text="     Shorthand     ", font=("Arial", 15)).grid(row=0, column=0, sticky='nsew')
tk.Label(title_frame, text="    Expands To     ", font=("Arial", 15)).grid(row=0, column=1, sticky='nsew')
tk.Label(title_frame, text="     ", font=("Arial", 15)).grid(row=0, column=2, sticky='nsew')
tk.Button(button_frame, text="Add Shorthand Entry", font=("Arial", 15), command=create_entry).grid(row=2, column=0, pady=10, padx=10) 

root.mainloop()
