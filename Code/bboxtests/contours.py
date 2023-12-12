#!/usr/bin/env python3

import sys

sys.path.append("../tools")
sys.path.append("../application")
from file_manager import file_manager
import cv2
import numpy as np
import imutils
import os

class contours:
    file_manager_operative = file_manager()
    _model = None
    _LB = None
    
    def __init__(self):
        self._LB = self.file_manager_operative.load_LabelBinarizer()
        self._model = self.file_manager_operative.load_ocr_model()
        
    def _hex_to_char(self, hex_input):
        return(chr(int(hex_input[0], 16)))

    def _sort_contours(self, cnts, method="left-to-right"):
        reverse = False
        i = 0
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b:b[1][i], reverse=reverse))

        return (cnts, boundingBoxes)

    def get_letters(self, img, line_thickness, analyzed_cell_directory):
        letters = []
        image = cv2.imread(img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        dilated = cv2.dilate(thresh1, None, iterations=line_thickness)

        cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = self._sort_contours(cnts, method="left-to-right")[0]

            box_expand = 2
            for c in cnts:
                if cv2.contourArea(c) > 275:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                    roi = gray[(y - box_expand):(y + h + box_expand), (x - box_expand):(x + w + box_expand)]
                    thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                    try:
                        thresh = cv2.resize(thresh, (32, 32), interpolation = cv2.INTER_CUBIC)
                        thresh = thresh.astype("float32") / 255.0
                        thresh = np.expand_dims(thresh, axis=-1)
                        thresh = thresh.reshape(1,32,32,1)
                        ypred = self._model.predict(thresh, verbose=0)
                        ypred = self._LB.inverse_transform(ypred)
                        [x] = self._hex_to_char(ypred)
                        letters.append(x)
                    except Exception as e:
                        pass
            cv2.imwrite(str(analyzed_cell_directory + "/" + os.path.basename(img)), image)
        return letters
