import tensorflow as tf
import cv2
import file_manager as fm
from sklearn.preprocessing import LabelBinarizer
import imutils
import numpy as np
import short_to_long as sl

global model, LB

def hex_to_char(hex_input):
    return(chr(int(hex_input[0], 16)))

def sort_contours(cnts, method="left-to-right"):
    reverse = False
    i = 0
    if method == "right-to-left" or method == "bottom-to-top":
        reverse = True
    if method == "top-to-bottom" or method == "bottom-to-top":
        i = 1
    boundingBoxes = [cv2.boundingRect(c) for c in cnts]
    (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b:b[1][i], reverse=reverse))

    return (cnts, boundingBoxes)

def get_letters(img):
    global model, LB
    letters = []
    image = cv2.imread(img)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret,thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    dilated = cv2.dilate(thresh1, None, iterations=3)

    cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) > 0:
        cnts = sort_contours(cnts, method="left-to-right")[0]

        box_expand = 2
        for c in cnts:
            if cv2.contourArea(c) > 125:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                roi = gray[(y - box_expand):(y + h + box_expand), (x - box_expand):(x + w + box_expand)]
                thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                thresh = cv2.resize(thresh, (32, 32), interpolation = cv2.INTER_CUBIC)
                thresh = thresh.astype("float32") / 255.0
                thresh = np.expand_dims(thresh, axis=-1)
                thresh = thresh.reshape(1,32,32,1)
                ypred = model.predict(thresh)
                ypred = LB.inverse_transform(ypred)
                [x] = hex_to_char(ypred)
                letters.append(x)
        return letters

def get_word(letters):
    word = ""
    if letters:
        for letter in letters:
            word += letter
    #word = "".join(letters)
    return word

def get_predictions():
    global model, LB
    LB = fm.load_LabelBinarizer()
    model = fm.load_ocr_model()
    predictions = []
    fm.delete_ignored_rows()
    cells = fm.get_storage()
    for cell in cells:
        letters = get_letters(cell)
        word = get_word(letters)
        print(word)
        predictions.append(word)

    predictions = sl.short_to_long(predictions)

    return predictions

