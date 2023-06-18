import pickle
from sklearn.preprocessing import LabelBinarizer
import os
import shutil

def save_shorthand(shorthand):
    pickle.dump(shorthand, open('shorthand.pkl', 'wb'))

def load_shorthand():
    shorthand = {}
    if(os.path.isfile('shorthand.pkl')):
        with open('shorthand.pkl', 'rb') as sh_load:
            shorthand = pickle.load(sh_load)
    
    return shorthand

def load_LabelBinarizer():
    LB = LabelBinarizer()
    with open('../../LabelBinarizer/LabelBinarizer.pkl') as LB_config:
        LB = pickle.load(LB_config)

    return LB

def clear_storage():
    folder = '../../Storage'
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
    folder = '../../Storage'
    for filename in os.listdir(folder):
        filenames.append(folder + '/' + filename)

    return filenames
