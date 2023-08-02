import pickle
import os
import shutil

class file_manager:
    __exe_path = ''

    def save_shorthand(self, shorthand):
        path = self.__exe_path + '../../Settings/shorthand.pkl'
        pickle.dump(shorthand, open(path, 'wb'))

    def load_shorthand(self):
        shorthand = {}
        path = self.__exe_path + '../../Settings/shorthand.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as sh_load:
                shorthand = pickle.load(sh_load)
    
        return shorthand

    def save_ignore(self, ignore):
        path = self.__exe_path + '../../Settings/ignore.pkl'
        pickle.dump(ignore, open(path, 'wb'))

    def load_ignore(self):
        ignore = []
        path = self.__exe_path + '../../Settings/ignore.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as ig_load:
                ignore = pickle.load(ig_load)
            
        return ignore

    def save_default_directory(self, default_directory):
        path = self.__exe_path + '../../Settings/default_directory.pkl'
        pickle.dump(default_directory, open(path, 'wb'))

    def load_default_directory(self):
        default_directory = ''
        path = self.__exe_path + '../../Settings/default_directory.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as dd_load:
                default_directory = pickle.load(dd_load)

        return default_directory

    def save_rows_columns(self, rows_columns):
        path = self.__exe_path + '../../Settings/rows_columns.pkl'
        pickle.dump(rows_columns, open(path, 'wb'))

    def load_rows_columns(self):
        rows_columns = []
        path = self.__exe_path + '../../Settings/rows_columns.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as rc_load:
                rows_columns = pickle.load(rc_load)

        return rows_columns

    def save_line_thickness(self, line_thickness):
        path = self.__exe_path + '../../Settings/line_thickness.pkl'
        pickle.dump(line_thickness, open(path, 'wb'))

    def load_line_thickness(self):
        line_thickness = "2"
        path = self.__exe_path + '../../Settings/line_thickness.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as lt_load:
                line_thickness = pickle.load(lt_load)

        return line_thickness

    def save_find_shorthand_matches(self, find_shorthand_matches):
        path = self.__exe_path + '../../Settings/find_shorthand_matches.pkl'
        pickle.dump(find_shorthand_matches, open(path, 'wb'))

    def load_find_shorthand_matches(self):
        find_shorthand_matches = 0
        path = self.__exe_path + '../../Settings/find_shorthand_matches.pkl'
        if(os.path.isfile(path)):
            with open(path, 'rb') as fsm_load:
                find_shorthand_matches = pickle.load(fsm_load)

        return find_shorthand_matches

    def clear_storage(self):
        folder = self.__exe_path + '../../Storage'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
            
    def get_storage(self):
        filenames = []
        folder = self.__exe_path + '../../Storage'
        for filename in os.listdir(folder):
            filenames.append(folder + '/' + filename)
        filenames = self.sort_storage(filenames)
        return filenames

    def sort_storage(self, filenames):
        sorted_filenames = []
        folder = self.__exe_path + '../../Storage/'
        for filename in filenames:
            num = filename.replace('.jpg', '')
            num = num.replace(folder , '')
            sorted_filenames.append(int(num))
        sorted_filenames.sort()
        for i in range(len(sorted_filenames)):
            sorted_filenames[i] = folder + str(sorted_filenames[i]) + '.jpg'
        return sorted_filenames
    

    def delete_ignored_rows(self):
        ignore = []
        ignore = self.load_ignore()
        rows_columns = []
        rows_columns = self.load_rows_columns()
        for page, row in ignore:
            start_cell = (int(page) - 1)*int(rows_columns[0])*int(rows_columns[1]) + (int(row) - 1)*int(rows_columns[1])
            stop_cell = start_cell + int(rows_columns[1])
            self.delete_cells_in_range(start_cell, stop_cell)

    def delete_cells_in_range(self, start_cell, stop_cell):
        folder = self.__exe_path + '../../Storage'
        for i in range(start_cell, stop_cell):
            filename = str(i) + ".jpg"
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
            
        
