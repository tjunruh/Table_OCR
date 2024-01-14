import tkinter as tk
from tkscrolledframe import ScrolledFrame
from file_manager import file_manager

class edit_common_entry:
    file_manager_operative = file_manager()
    __root = None
    __title_frame = None
    __button_frame = None
    __scroll_frame = None
    __edit_frame = None
    __button_frame2 = None
    __rows = None
    __common_entry_list = None
    __common_entries = None

    def __delete_entry(self, entry, button):
        index = 0
        for e, b in self.__common_entry_list:
            if ((e == entry) and (b == button)):
                e.destroy()
                b.destroy()
                self.__common_entry_list.pop(index)
                self.__rows -= 1

            index += 1

    def __create_entry(self):
        row = self.__rows
        entry=tk.Entry(self.__edit_frame, font=("Arial", 10), width=48)
        button=tk.Button(self.__edit_frame, text="  X  ", font=("Arial", 10), command=lambda :self.__delete_entry(entry, button))
        self.__common_entry_list.append([entry, button])
        self.__common_entry_list[row][0].grid(row=self.__rows, column=0, sticky='nsew')
        self.__common_entry_list[row][1].grid(row=self.__rows, column=1, sticky='nsew')
        self.__edit_frame.rowconfigure(self.__rows, weight=1)
        self.__rows += 1

    def __initialize(self):
        self.__common_entries = []
        self.__common_entry_list = []
        self.__rows = 0
        self.__common_entries = self.file_manager_operative.load_common_entries()
        for common_entry in self.__common_entries:
            self.__create_entry()
            row = self.__rows - 1
            self.__common_entry_list[row][0].insert(0,common_entry)

    def __close(self):
        self.__root.grab_release()
        self.__root.destroy()

    def __ok(self):
        self.__common_entries.clear()
        for e, b in self.__common_entry_list:
            if(e.get() != "" and e.get() not in self.__common_entries):
                self.__common_entries.append(e.get())
        self.file_manager_operative.save_common_entries(self.__common_entries)
        self.__close()
    
    def run(self):
        self.__root = tk.Toplevel()
        self.__root.grab_set()

        self.__root.title("Edit Common Entry")
        self.__root.rowconfigure(4, weight=1)
        self.__root.columnconfigure(1, weight=1)

        self.__title_frame = tk.Frame(self.__root)
        self.__title_frame.rowconfigure(0, weight=1)
        self.__title_frame.columnconfigure(0, weight=1)
        self.__title_frame.grid(row=0, column=0, sticky='nsew')

        self.__button_frame = tk.Frame(self.__root)
        self.__button_frame.rowconfigure(0, weight=1)
        self.__button_frame.columnconfigure(0, weight=1)
        self.__button_frame.grid(row=2, column=0, sticky='nsew')

        self.__button_frame2 = tk.Frame(self.__root)
        self.__button_frame2.rowconfigure(0, weight=1)
        self.__button_frame2.columnconfigure(1, weight=1)
        self.__button_frame2.grid(row=3, column=0, sticky='nsew')

        self.__scroll_frame = ScrolledFrame(self.__root)
        self.__scroll_frame.grid(row=1, column=0, sticky='nsew')
        self.__scroll_frame.bind_arrow_keys(self.__root)
        self.__scroll_frame.bind_scroll_wheel(self.__root)
        self.__edit_frame = self.__scroll_frame.display_widget(tk.Frame)
        self.__edit_frame.rowconfigure(1, weight=1)
        self.__edit_frame.columnconfigure(3, weight=1)

        tk.Label(self.__title_frame, text="   Common Entry   ", font=("Arial", 15)).grid(row=0, column=0, sticky='nsew')
        tk.Label(self.__title_frame, text="     ", font=("Arial", 15)).grid(row=0, column=2, sticky='nsew')
        tk.Button(self.__button_frame, text=" Add Common Entry ", font=("Arial", 15), command=self.__create_entry).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self.__button_frame2, text="        OK        ", font=("Arial", 15), command=self.__ok).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self.__button_frame2, text="      Cancel      ", font=("Arial", 15), command=self.__close).grid(row=0, column=1, pady=10, padx=10)

        self.__initialize()

        self.__root.protocol("WM_DELETE_WINDOW", self.__close)
        self.__root.mainloop()


