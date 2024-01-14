import tkinter as tk
from tkscrolledframe import ScrolledFrame
from file_manager import file_manager

class edit_shorthand:
    file_manager_operative = file_manager()
    __root = None
    __title_frame = None
    __button_frame = None
    __scroll_frame = None
    __edit_frame = None
    __button_frame2 = None
    __rows = None
    __shorthand_list = None
    __shorthand = None

    def __delete_entry(self, entry1, entry2, button1):
        index = 0
        for e1, e2, b1 in self.__shorthand_list:
            if ((e1 == entry1) and (e2 == entry2) and (b1 == button1)):
                e1.destroy()
                e2.destroy()
                b1.destroy()
                self.__shorthand_list.pop(index)
                self.__rows -= 1

            index += 1

    def __create_entry(self):
        row = self.__rows
        entry1=tk.Entry(self.__edit_frame, font=("Arial", 10), width=24)
        entry2=tk.Entry(self.__edit_frame, font=("Arial", 10), width=24)
        button1=tk.Button(self.__edit_frame, text="  X  ", font=("Arial", 10), command=lambda :self.__delete_entry(entry1, entry2, button1))
        self.__shorthand_list.append([entry1, entry2, button1])
        self.__shorthand_list[row][0].grid(row=self.__rows, column=0, sticky='nsew')
        self.__shorthand_list[row][1].grid(row=self.__rows, column=1, sticky='nsew')
        self.__shorthand_list[row][2].grid(row=self.__rows, column=2, sticky='nsew')
        self.__edit_frame.rowconfigure(self.__rows, weight=1)
        self.__rows += 1

    def __initialize(self):
        self.__shorthand = {}
        self.__shorthand_list = []
        self.__rows = 0
        self.__shorthand = self.file_manager_operative.load_shorthand()
        for short, long in self.__shorthand.items():
            self.__create_entry()
            row = self.__rows - 1
            self.__shorthand_list[row][0].insert(0,short)
            self.__shorthand_list[row][1].insert(0,long)

    def __close(self):
        self.__root.grab_release()
        self.__root.destroy()

    def __ok(self):
        self.__shorthand.clear()
        for e1, e2, b1 in self.__shorthand_list:
            if((e1.get() != "") and (e2.get() != "") and (e1.get() not in self.__shorthand.keys())):
                self.__shorthand[e1.get()] = e2.get()
        self.file_manager_operative.save_shorthand(self.__shorthand)
        self.__close()

    def run(self):
        self.__root = tk.Toplevel()
        self.__root.grab_set()

        self.__root.title("Edit Shorthand")
        self.__root.rowconfigure(4, weight=1)
        self.__root.columnconfigure(1, weight=1)

        self.__title_frame = tk.Frame(self.__root)
        self.__title_frame.rowconfigure(0, weight=1)
        self.__title_frame.columnconfigure(1, weight=1)
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

        tk.Label(self.__title_frame, text="     Shorthand     ", font=("Arial", 15)).grid(row=0, column=0, sticky='nsew')
        tk.Label(self.__title_frame, text="    Expands To     ", font=("Arial", 15)).grid(row=0, column=1, sticky='nsew')
        tk.Label(self.__title_frame, text="     ", font=("Arial", 15)).grid(row=0, column=2, sticky='nsew')
        tk.Button(self.__button_frame, text="Add Shorthand Entry", font=("Arial", 15), command=self.__create_entry).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self.__button_frame2, text="        OK         ", font=("Arial", 15), command=self.__ok).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self.__button_frame2, text="      Cancel       ", font=("Arial", 15), command=self.__close).grid(row=0, column=1, pady=10, padx=10)

        self.__initialize()

        self.__root.protocol("WM_DELETE_WINDOW", self.__close)
        self.__root.mainloop()

