import pickle
from sklearn.preprocessing import LabelBinarizer
import os
import shutil
from tensorflow.keras.models import load_model

exe_path = ''

def save_shorthand(shorthand):
    path = exe_path + '../../Settings/shorthand.pkl'
    pickle.dump(shorthand, open(path, 'wb'))

def load_shorthand():
    shorthand = {}
    path = exe_path + '../../Settings/shorthand.pkl'
    if(os.path.isfile(path)):
        with open(path, 'rb') as sh_load:
            shorthand = pickle.load(sh_load)
    
    return shorthand

def save_ignore(ignore):
    path = exe_path + '../../Settings/ignore.pkl'
    pickle.dump(ignore, open(path, 'wb'))

def load_ignore():
    ignore = []
    path = exe_path + '../../Settings/ignore.pkl'
    if(os.path.isfile(path)):
        with open(path, 'rb') as ig_load:
            ignore = pickle.load(ig_load)
            
    return ignore

def save_default_directory(default_directory):
    path = exe_path + '../../Settings/default_directory.pkl'
    pickle.dump(default_directory, open(path, 'wb'))

def load_default_directory():
    default_directory = ''
    path = exe_path + '../../Settings/default_directory.pkl'
    if(os.path.isfile(path)):
        with open(path, 'rb') as dd_load:
            default_directory = pickle.load(dd_load)

    return default_directory

def save_rows_columns(rows_columns):
    path = exe_path + '../../Settings/rows_columns.pkl'
    pickle.dump(rows_columns, open(path, 'wb'))

def load_rows_columns():
    rows_columns = []
    path = exe_path + '../../Settings/rows_columns.pkl'
    if(os.path.isfile(path)):
        with open(path, 'rb') as rc_load:
            rows_columns = pickle.load(rc_load)

    return rows_columns

def load_LabelBinarizer():
    LB = LabelBinarizer()
    path = exe_path + '../../LabelBinarizer/LabelBinarizer.pkl'
    with open(path, 'rb') as LB_config:
        LB = pickle.load(LB_config)

    return LB

def load_ocr_model():
    path = exe_path + "../../Model"
    model = load_model(path)
    return model

def clear_storage():
    folder = exe_path + '../../Storage'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
            
def get_storage():
    filenames = []
    folder = exe_path + '../../Storage'
    for filename in os.listdir(folder):
        filenames.append(folder + '/' + filename)
    filenames = sort_storage(filenames)
    return filenames

def sort_storage(filenames):
    sorted_filenames = []
    folder = exe_path + '../../Storage/'
    for filename in filenames:
        num = filename.replace('.jpg', '')
        num = num.replace(folder , '')
        sorted_filenames.append(int(num))
    sorted_filenames.sort()
    for i in range(len(sorted_filenames)):
        sorted_filenames[i] = folder + str(sorted_filenames[i]) + '.jpg'
    return sorted_filenames
    

def delete_ignored_rows():
    ignore = []
    ignore = load_ignore()
    rows_columns = []
    rows_columns = load_rows_columns()
    for page, row in ignore:
        start_cell = (int(page) - 1)*int(rows_columns[0])*int(rows_columns[1]) + (int(row) - 1)*int(rows_columns[1])
        stop_cell = start_cell + int(rows_columns[1])
        delete_cells_in_range(start_cell, stop_cell)

def delete_cells_in_range(start_cell, stop_cell):
    folder = exe_path + '../../Storage'
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
            
        
