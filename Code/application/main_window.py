import tkinter as tk
from file_manager import file_manager
from ignore_rows import ignore_rows
from edit_shorthand import edit_shorthand
from default_directory import default_directory
from table_display import table_display
from table_extractor import table_extractor
from predict import predict
from tkinter import filedialog
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import messagebox

class main_window:
    ignore_rows_window = ignore_rows()
    edit_shorthand_window = edit_shorthand()
    default_directory_window = default_directory()
    extract_cells_operative = table_extractor()
    table_display_window = table_display()
    predict_operative = predict()
    file_manager_operative = file_manager()
    __root = None
    __select_file_frame = None
    __display_file_frame = None
    __row_column_frame = None
    __line_thickness_frame = None
    __generate_frame = None
    __rows = None
    __columns = None
    __file_display = None
    __file_name = None
    __pb = None
    __line_thickness = None
    __find_shorthand_matches = None
    __rows_columns = None
        
    def __close(self):
        self.__rows_columns.clear()
        self.file_manager_operative.save_line_thickness(self.__line_thickness.get())
        self.file_manager_operative.save_find_shorthand_matches(self.__find_shorthand_matches.get())
        if((str(self.__rows.get()).isnumeric()) and (str(self.__columns.get()).isnumeric())):
            self.__rows_columns.append(self.__rows.get())
            self.__rows_columns.append(self.__columns.get())
            self.file_manager_operative.save_rows_columns(self.__rows_columns)
        self.__root.destroy()

    def __chose_pdf(self):
        self.__file_name = filedialog.askopenfilename(initialdir = self.file_manager_operative.load_default_directory(), title = "Select a File")
        self.__file_display.set(self.__file_name)

    def __run_edit_shorthand(self):
        self.edit_shorthand_window.run()

    def __run_ignore_rows(self):
        self.ignore_rows_window.run()

    def __run_default_directory(self):
        self.default_directory_window.run()

    def __predict_error(self):
        messagebox.showerror('Could not run predictions', '- Do you have rows and columns set correctly?\n- Are you ignoring all rows that need to be ignored?\n- Did you select a valid pdf?')

    def __extract_error(self):
        messagebox.showerror('Could not extract cells', 'You must select a PDF file')

    def __generate_table(self):
        self.__root.update_idletasks()
        self.__rows_columns.clear()
        self.__rows_columns.append(self.__rows.get())
        self.__rows_columns.append(self.__columns.get())
        self.file_manager_operative.save_rows_columns(self.__rows_columns)
        ignore = []
        ignore = self.file_manager_operative.load_ignore()
        if self.extract_cells_operative.extract_cells(self.__file_name, self.__extract_error) != -1:
            predictions = self.predict_operative.get_predictions(self.__root, self.__pb, self.__predict_error, int(self.__line_thickness.get()), self.__find_shorthand_matches.get())
            self.file_manager_operative.clear_storage()
            if predictions:
                self.table_display_window.run(predictions, int(self.__columns.get()))
     
    def run(self):
        self.__file_name = ""
        self.__root = tk.Tk()

        self.__root.title("Handwritten Table Interpreter")
        self.__root.rowconfigure(6, weight=1)
        self.__root.columnconfigure(2, weight=1)

        menubar = tk.Menu(self.__root)
        menubar.add_command(label="Edit Shorthand", command=self.__run_edit_shorthand)
        menubar.add_command(label="Ignore Rows", command=self.__run_ignore_rows)
        menubar.add_command(label="Default Directory", command=self.__run_default_directory)
    
        self.__root.config(menu=menubar)
    

        self.__select_file_frame = tk.Frame(self.__root)
        self.__select_file_frame.rowconfigure(0, weight=1)
        self.__select_file_frame.columnconfigure(0, weight=1)
        self.__select_file_frame.grid(row=0, column=0, sticky='nsew')

        self.__display_file_frame = tk.Frame(self.__root)
        self.__display_file_frame.rowconfigure(0, weight=1)
        self.__display_file_frame.columnconfigure(0, weight=1)
        self.__display_file_frame.grid(row=1, column=0, sticky='nsew')

        self.__row_column_frame = tk.Frame(self.__root)
        self.__row_column_frame.rowconfigure(1, weight=1)
        self.__row_column_frame.columnconfigure(1, weight=1)
        self.__row_column_frame.grid(row=2, column=0, sticky='nsew')

        self.__line_thickness_frame = tk.Frame(self.__root)
        self.__line_thickness_frame.rowconfigure(0, weight=1)
        self.__line_thickness_frame.columnconfigure(0, weight=1)
        self.__line_thickness_frame.grid(row=3, column=0, sticky='nsew')

        self.__generate_frame = tk.Frame(self.__root)
        self.__generate_frame.rowconfigure(0, weight=1)
        self.__generate_frame.columnconfigure(0, weight=1)
        self.__generate_frame.grid(row=4, column=0, sticky='nsew')

        self.__pb = ttk.Progressbar(self.__root, orient='horizontal', mode='determinate', length=280)
        self.__pb.grid(row=5, column=0, padx=10, pady=20)

        self.__rows_columns = []
        self.__rows_columns = self.file_manager_operative.load_rows_columns()
        self.__rows = tk.StringVar(self.__root)
        self.__columns = tk.StringVar(self.__root)

        if self.__rows_columns:
            self.__rows.set(self.__rows_columns[0])
            self.__columns.set(self.__rows_columns[1])

        self.__file_display = tk.StringVar(self.__root)
    
        tk.Button(self.__select_file_frame, text="Select PDF", font=("Arial", 15), command=self.__chose_pdf).grid(row=0, column=0, pady=10, padx=10)
        tk.Label(self.__display_file_frame, font=("Arial", 12), textvariable=self.__file_display).grid(row=0, column=0, pady=10, padx=10)
        tk.Label(self.__row_column_frame, text="Rows in Table:", font=("Arial", 15)).grid(row=0, column=0, pady=5, padx=15)
        tk.Label(self.__row_column_frame, text="Columns in Table:", font=("Arial", 15)).grid(row=0, column=1, pady=5, padx=15)
        tk.Spinbox(self.__row_column_frame, from_=1, to=100, increment=1.0, textvariable=self.__rows, font=("Arial", 15), state='readonly').grid(row=1, column=0, pady=5, padx=15)
        tk.Spinbox(self.__row_column_frame, from_=1, to=100, increment=1.0, textvariable=self.__columns, font=("Arial", 15), state='readonly').grid(row=1, column=1, pady=5, padx=15)

        self.__line_thickness = tk.StringVar(self.__root, self.file_manager_operative.load_line_thickness())
        ttk.Separator(self.__line_thickness_frame, orient='horizontal').pack(fill='x')
        tk.Label(self.__line_thickness_frame, text="Handwriting Thickness", font=("Arial", 15)).pack(side=tk.TOP, ipady=5)
        
        values = {"Thin" : "2",
                  "Normal" : "3",
                  "Thick" : "4"}

        for text, value in values.items():
            tk.Radiobutton(self.__line_thickness_frame, text=text, variable=self.__line_thickness, value=value, font=("Arial", 15)).pack(side=tk.TOP, ipady=5)

        ttk.Separator(self.__line_thickness_frame, orient='horizontal').pack(fill='x')
        self.__find_shorthand_matches = tk.IntVar(self.__root, self.file_manager_operative.load_find_shorthand_matches())
        tk.Checkbutton(self.__line_thickness_frame, text="Find shorthand matches", variable=self.__find_shorthand_matches, onvalue=1, offvalue=0, font=("Arial", 15)).pack(side=tk.TOP, ipady=5)

        ttk.Separator(self.__line_thickness_frame, orient='horizontal').pack(fill='x')
        
        tk.Button(self.__generate_frame, text="Generate Tables", font=("Arial", 15), command=self.__generate_table).grid(row=0, column=0, pady=5, padx=5)
                         
        self.__root.protocol("WM_DELETE_WINDOW", self.__close)
        self.__root.mainloop()

if __name__ == "__main__":
    Table_OCR = main_window()
    Table_OCR.run()
