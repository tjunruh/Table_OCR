import pickle
from sklearn.preprocessing import LabelBinarizer
import os
import shutil
from tensorflow.keras.models import load_model

exe_path = '../../'

def save_shorthand(shorthand):
    pickle.dump(shorthand, open('shorthand.pkl', 'wb'))

def load_shorthand():
    shorthand = {}
    if(os.path.isfile('shorthand.pkl')):
        with open('shorthand.pkl', 'rb') as sh_load:
            shorthand = pickle.load(sh_load)
    
    return shorthand

def save_ignore(ignore):
    pickle.dump(ignore, open('ignore.pkl', 'wb'))

def load_ignore():
    ignore = []
    if(os.path.isfile('ignore.pkl')):
        with open('ignore.pkl', 'rb') as ig_load:
            ignore = pickle.load(ig_load)
            
    return ignore

def save_default_directory(default_directory):
    pickle.dump(default_directory, open('default_directory.pkl', 'wb'))

def load_default_directory():
    default_directory = ''
    if(os.path.isfile('default_directory.pkl')):
        with open('default_directory.pkl', 'rb') as dd_load:
            default_directory = pickle.load(dd_load)

    return default_directory

def save_rows_columns(rows_columns):
    pickle.dump(rows_columns, open('rows_columns.pkl', 'wb'))

def load_rows_columns():
    rows_columns = []
    if(os.path.isfile('rows_columns.pkl')):
        with open('rows_columns.pkl', 'rb') as rc_load:
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
            
        
