from tksheet import Sheet
import tkinter as tk
from short_to_long import short_to_long

class table_display:
    short_to_long_operative = short_to_long()
    __root = None
    __frame = None
    __cells = None
    __sheet = None

    def __update_cell(self, event):
        row, column, mode, value, *_ = event
        currently_selected = self.__sheet.get_currently_selected()
        if currently_selected:
            if currently_selected.type_ == "cell":
                word = self.short_to_long_operative.single_short_to_long(value)
                self.__sheet.set_cell_data(row, column, value=word, redraw=True)
        
        

    def run(self, predictions, columns):
        rows = int(len(predictions)/columns)
        self.__root = tk.Tk()
        self.__root.geometry("1400x700")
        self.__root.grid_columnconfigure(0, weight = 1)
        self.__root.grid_rowconfigure(0, weight = 1)
        self.__frame = tk.Frame(self.__root)
        self.__frame.grid_columnconfigure(0, weight = 1)
        self.__frame.grid_rowconfigure(0, weight = 1)
        self.__cells = [[predictions[c + (r * columns)] for c in range(columns)] for r in range(rows)]
        self.__sheet = Sheet(self.__frame, data=self.__cells)
        self.__sheet.set_all_column_widths(130)
        self.__sheet.enable_bindings()
        self.__sheet.font(newfont = ("century Gothic", 9, "normal"))
        self.__frame.grid(row=0, column=0, sticky="nsew")
        self.__sheet.grid(row=0, column=0, sticky="nsew")

        self.__sheet.extra_bindings('end_edit_cell', func=self.__update_cell)

        self.__root.mainloop()
