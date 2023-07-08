import tkinter as tk
from file_manager import file_manager
import os
from tkinter import messagebox

class default_directory:
    file_manager_operative = file_manager()
    __root = None
    __entry_frame = None
    __button_frame = None
    __entry = None
    
    def __close(self):
        self.__root.grab_release()
        self.__root.destroy()

    def __ok(self):
        if ((os.path.isdir(self.__entry.get())) and (self.__entry.get() != '')):
            default_directory = self.__entry.get()
            self.file_manager_operative.save_default_directory(default_directory)
            self.__close()
        else:
            messagebox.showerror('Error', 'Not a directory')

    def run(self):
        self.__root = tk.Toplevel()
        self.__root.grab_set()

        self.__root.title("Default Directory")
        self.__root.rowconfigure(2, weight=1)
        self.__root.columnconfigure(1, weight=1)

        self.__entry_frame = tk.Frame(self.__root)
        self.__entry_frame.rowconfigure(0, weight=1)
        self.__entry_frame.columnconfigure(0, weight=1)
        self.__entry_frame.grid(row=0, column=0, sticky='nsew')

        self.__button_frame = tk.Frame(self.__root)
        self.__button_frame.rowconfigure(0, weight=1)
        self.__button_frame.columnconfigure(1, weight=1)
        self.__button_frame.grid(row=1, column=0, sticky='nsew')

        self.__entry = tk.Entry(self.__entry_frame, font=("Arial", 10), width=48)
        self.__entry.grid(row=0, column=0, pady=10, padx=10)
        self.__entry.insert(0, self.file_manager_operative.load_default_directory())
        tk.Button(self.__button_frame, text="        OK         ", font=("Arial", 15), command=self.__ok).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(self.__button_frame, text="      Cancel       ", font=("Arial", 15), command=self.__close).grid(row=0, column=1, padx=10, pady=10)

        self.__root.protocol("WM_DELETE_WINDOW", self.__close)
        self.__root.mainloop()
    
