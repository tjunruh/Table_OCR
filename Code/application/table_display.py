from tksheet import Sheet
import tkinter as tk
from short_to_long import short_to_long
from file_manager import file_manager

class table_display:
    short_to_long_operative = short_to_long()
    file_manager_operative = file_manager()
    
    __root = None
    __frame = None
    __cells = None
    __sheet = None
    __original_predictions = []
    __bounding_boxes = []
    __columns = None
    __valid_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y']

    def __update_cell(self, event):
        row, column, mode, value, *_ = event
        columns = self.__sheet.get_column_data(column)
        currently_selected = self.__sheet.get_currently_selected()
        if currently_selected:
            if currently_selected.type_ == "cell":
                column_data = self.__sheet.get_column_data(column)
                word = self.short_to_long_operative.single_short_to_long(value, column_data[0:row])
                self.__sheet.set_cell_data(row, column, value=word, redraw=True)
                index = self.__get_index(row, column)
                if index < len(self.__original_predictions):
                    if self.__original_predictions[index] != '1' and self.__original_predictions[index] != 'I' and len(value) == len(self.__original_predictions[index]):
                        value = value.upper()
                        value = self.short_to_long_operative.inverse_char_set(value)
                        valid_string = True
                        for char in value:
                            if char not in self.__valid_chars:
                                valid_string = False
                                break
                        if valid_string and self.file_manager_operative.get_number_of_training_images() < 1000:     
                            self.file_manager_operative.save_training_image(index, value, self.__bounding_boxes[index])
                    
        
    def __get_index(self, row, column):
        index = self.__columns * row + column
        return index

    def run(self, predictions_displayed, columns, bounding_boxes, original_predictions):
        self.__original_predictions = original_predictions
        self.__bounding_boxes = bounding_boxes
        self.__columns = columns
        rows = int(len(predictions_displayed)/columns)
        self.__root = tk.Tk()
        self.__root.geometry("1400x700")
        self.__root.grid_columnconfigure(0, weight = 1)
        self.__root.grid_rowconfigure(0, weight = 1)
        self.__frame = tk.Frame(self.__root)
        self.__frame.grid_columnconfigure(0, weight = 1)
        self.__frame.grid_rowconfigure(0, weight = 1)
        self.__cells = [[predictions_displayed[c + (r * columns)] for c in range(columns)] for r in range(rows)]
        self.__sheet = Sheet(self.__frame, data=self.__cells)
        self.__sheet.set_all_column_widths(130)
        self.__sheet.enable_bindings()
        self.__sheet.font(newfont = ("century Gothic", 9, "normal"))
        self.__frame.grid(row=0, column=0, sticky="nsew")
        self.__sheet.grid(row=0, column=0, sticky="nsew")

        self.__sheet.extra_bindings('end_edit_cell', func=self.__update_cell)

        self.__root.mainloop()
