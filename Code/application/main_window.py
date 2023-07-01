import tkinter as tk
import file_manager as fm
import ignore_rows as ir
import edit_shorthand as es
import short_to_long as sl
import table_display as td
import table_extractor as te
import predict as p
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox

global root, select_file_frame, display_file_frame, row_column_frame, generate_frame, rows, columns, file_display, file_name, menu, pb
global rows_columns

def close():
    global root, select_file_frame, display_file_frame, row_column_frame, generate_frame, rows, columns, file_display, file_name, menu
    global rows_columns
    rows_columns.clear()
    if((str(rows.get()).isnumeric()) and (str(columns.get()).isnumeric())):
        rows_columns.append(rows.get())
        rows_columns.append(columns.get())
        fm.save_rows_columns(rows_columns)
    root.destroy()

def chose_pdf():
    global file_display, filename
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File")
    file_display.set(filename)

def run_edit_shorthand():
    es.run()

def run_ignore_rows():
    ir.run()

def error():
    messagebox.showerror('Could not run predictions', 'Do you have rows and columns set correctly?\nAre you ignoring all rows that need to be ignored?')

def generate_table():
    global rows, columns, filename, rows_columns, pb
    root.update_idletasks()
    if((str(rows.get()).isnumeric()) and (str(columns.get()).isnumeric())):
        rows_columns.append(rows.get())
        rows_columns.append(columns.get())
        fm.save_rows_columns(rows_columns)
    ignore = []
    ignore = fm.load_ignore()
    te.extract_cells(filename)
    predictions = p.get_predictions(root, pb, error)
    fm.clear_storage()
    if predictions:
        td.run(predictions, int(columns.get()))
     
def run():
    global root, select_file_frame, display_file_frame, row_column_frame, generate_frame, rows, columns, file_display, file_name, menu, pb
    global rows_columns
    root = tk.Tk()

    root.title("Handwritten Table Interpreter")
    root.rowconfigure(4, weight=1)
    root.columnconfigure(2, weight=1)

    menubar = tk.Menu(root)
    menubar.add_command(label="Edit Shorthand", command=run_edit_shorthand)
    menubar.add_command(label="Ignore Rows", command=run_ignore_rows)
    
    root.config(menu=menubar)
    

    select_file_frame = tk.Frame(root)
    select_file_frame.rowconfigure(0, weight=1)
    select_file_frame.columnconfigure(0, weight=1)
    select_file_frame.grid(row=0, column=0, sticky='nsew')

    display_file_frame = tk.Frame(root)
    display_file_frame.rowconfigure(0, weight=1)
    display_file_frame.columnconfigure(0, weight=1)
    display_file_frame.grid(row=1, column=0, sticky='nsew')

    row_column_frame = tk.Frame(root)
    row_column_frame.rowconfigure(1, weight=1)
    row_column_frame.columnconfigure(1, weight=1)
    row_column_frame.grid(row=2, column=0, sticky='nsew')

    generate_frame = tk.Frame(root)
    generate_frame.rowconfigure(0, weight=1)
    generate_frame.columnconfigure(0, weight=1)
    generate_frame.grid(row=3, column=0, sticky='nsew')

    pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
    pb.grid(row=4, column=0, padx=10, pady=20)

    rows_columns = []
    rows_columns = fm.load_rows_columns()
    rows = tk.StringVar(root)
    columns = tk.StringVar(root)

    if rows_columns:
        rows.set(rows_columns[0])
        columns.set(rows_columns[1])

    file_display = tk.StringVar(root)
    
    tk.Button(select_file_frame, text="Select PDF", font=("Arial", 15), command=chose_pdf).grid(row=0, column=0, pady=10, padx=10)
    tk.Label(display_file_frame, font=("Arial", 12), textvariable=file_display).grid(row=0, column=0, pady=10, padx=10)
    tk.Label(row_column_frame, text="Rows in Table:", font=("Arial", 15)).grid(row=0, column=0, pady=5, padx=15)
    tk.Label(row_column_frame, text="Columns in Table:", font=("Arial", 15)).grid(row=0, column=1, pady=5, padx=15)
    tk.Spinbox(row_column_frame, from_=0, to=100, increment=1.0, textvariable=rows, font=("Arial", 15)).grid(row=1, column=0, pady=5, padx=15)
    tk.Spinbox(row_column_frame, from_=0, to=100, increment=1.0, textvariable=columns, font=("Arial", 15)).grid(row=1, column=1, pady=5, padx=15)
    tk.Button(generate_frame, text="Generate Tables", font=("Arial", 15), command=generate_table).grid(row=0, column=0, pady=5, padx=5)
                         
    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()
