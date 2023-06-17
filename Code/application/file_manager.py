import pickle
from sklearn.preprocessing import LabelBinarizer
import os.path

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

