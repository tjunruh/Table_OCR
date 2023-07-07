import tkinter as tk
import file_manager as fm
import ignore_rows as ir
import edit_shorthand as es
import default_directory as dd
import short_to_long as sl
import table_display as td
import table_extractor as te
import predict as p
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox

global root, select_file_frame, display_file_frame, row_column_frame, line_thickness_frame, generate_frame, rows, columns, file_display, file_name, menu, pb, line_thickness, find_shorthand_matches
global rows_columns

def close():
    global root, select_file_frame, display_file_frame, row_column_frame, line_thickness_frame, generate_frame, rows, columns, file_display, file_name, menu, line_thickness, find_shorthand_matches
    global rows_columns
    rows_columns.clear()
    fm.save_line_thickness(line_thickness.get())
    fm.save_find_shorthand_matches(find_shorthand_matches.get())
    if((str(rows.get()).isnumeric()) and (str(columns.get()).isnumeric())):
        rows_columns.append(rows.get())
        rows_columns.append(columns.get())
        fm.save_rows_columns(rows_columns)
    root.destroy()

def chose_pdf():
    global file_display, file_name
    file_name = filedialog.askopenfilename(initialdir = fm.load_default_directory(), title = "Select a File")
    file_display.set(file_name)

def run_edit_shorthand():
    es.run()

def run_ignore_rows():
    ir.run()

def run_default_directory():
    dd.run()

def predict_error():
    messagebox.showerror('Could not run predictions', '- Do you have rows and columns set correctly?\n- Are you ignoring all rows that need to be ignored?\n- Did you select a valid pdf?')

def extract_error():
    messagebox.showerror('Could not extract cells', 'You must select a PDF file')

def generate_table():
    global rows, columns, file_name, rows_columns, pb, find_shorthand_matches
    root.update_idletasks()
    rows_columns.clear()
    rows_columns.append(rows.get())
    rows_columns.append(columns.get())
    fm.save_rows_columns(rows_columns)
    ignore = []
    ignore = fm.load_ignore()
    if te.extract_cells(file_name, extract_error) != -1:
        predictions = p.get_predictions(root, pb, predict_error, int(line_thickness.get()), find_shorthand_matches.get())
        fm.clear_storage()
        if predictions:
            td.run(predictions, int(columns.get()))
     
def run():
    global root, select_file_frame, display_file_frame, row_column_frame, line_thickness_frame, generate_frame, rows, columns, file_display, file_name, menu, pb, line_thickness, find_shorthand_matches
    global rows_columns
    file_name = ""
    root = tk.Tk()

    root.title("Handwritten Table Interpreter")
    root.rowconfigure(6, weight=1)
    root.columnconfigure(2, weight=1)

    menubar = tk.Menu(root)
    menubar.add_command(label="Edit Shorthand", command=run_edit_shorthand)
    menubar.add_command(label="Ignore Rows", command=run_ignore_rows)
    menubar.add_command(label="Default Directory", command=run_default_directory)
    
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

    line_thickness_frame = tk.Frame(root)
    line_thickness_frame.rowconfigure(0, weight=1)
    line_thickness_frame.columnconfigure(0, weight=1)
    line_thickness_frame.grid(row=3, column=0, sticky='nsew')

    generate_frame = tk.Frame(root)
    generate_frame.rowconfigure(0, weight=1)
    generate_frame.columnconfigure(0, weight=1)
    generate_frame.grid(row=4, column=0, sticky='nsew')

    pb = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=280)
    pb.grid(row=5, column=0, padx=10, pady=20)

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
    tk.Spinbox(row_column_frame, from_=1, to=100, increment=1.0, textvariable=rows, font=("Arial", 15), state='readonly').grid(row=1, column=0, pady=5, padx=15)
    tk.Spinbox(row_column_frame, from_=1, to=100, increment=1.0, textvariable=columns, font=("Arial", 15), state='readonly').grid(row=1, column=1, pady=5, padx=15)

    line_thickness = tk.StringVar(root, fm.load_line_thickness())
    ttk.Separator(line_thickness_frame, orient='horizontal').pack(fill='x')
    tk.Label(line_thickness_frame, text="Handwriting Thickness", font=("Arial", 15)).pack(side=tk.TOP, ipady=5)
    values = {"Thin" : "2",
              "Normal" : "3",
              "Thick" : "4"}

    for text, value in values.items():
        tk.Radiobutton(line_thickness_frame, text=text, variable=line_thickness, value=value, font=("Arial", 15)).pack(side=tk.TOP, ipady=5)

    ttk.Separator(line_thickness_frame, orient='horizontal').pack(fill='x')
    find_shorthand_matches = tk.IntVar(root, fm.load_find_shorthand_matches())
    tk.Checkbutton(line_thickness_frame, text="Find shorthand matches", variable=find_shorthand_matches, onvalue=1, offvalue=0, font=("Arial", 15)).pack(side=tk.TOP, ipady=5)

    ttk.Separator(line_thickness_frame, orient='horizontal').pack(fill='x')
        
    tk.Button(generate_frame, text="Generate Tables", font=("Arial", 15), command=generate_table).grid(row=0, column=0, pady=5, padx=5)
                         
    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()

if __name__ == "__main__":
    run()
