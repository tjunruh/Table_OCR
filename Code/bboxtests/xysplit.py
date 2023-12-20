#!/usr/bin/env python3

import sys

import skimage

sys.path.append("../tools")
sys.path.append("../application")
from file_manager import file_manager
import cv2
import numpy as np
import os
    
def draw_box(src, x, y, h, w, r=0, g=200, b=0, a=0.4):
    overlay = src.copy()
    cv2.rectangle(overlay, (y, x), (y + w, x + h), (r, g, b),
                  -1)
    return cv2.addWeighted(overlay, a, src, 1 - a, 0)

class XYsplit:
    file_manager_operative = file_manager()
    __model = None
    __LB = None

    def __init__(self):
        self.__LB = self.file_manager_operative.load_LabelBinarizer()
        self.__model = self.file_manager_operative.load_ocr_model()
    
    def __hex_to_char(self, hex_input):
        return(chr(int(hex_input[0], 16)))

    def get_letters(self, img, analyzed_cell_directory):
        letters = []
        image_orig = cv2.imread(img)
        image_gray = cv2.cvtColor(image_orig, cv2.COLOR_BGR2GRAY)
        h, w = image_gray.shape
        _, image_bin = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        image_bin = cv2.erode(image_bin, np.ones((2, 2), np.uint8), iterations=1)
        image_bin = cv2.dilate(image_bin, np.ones((3, 3), np.uint8), iterations=1)
        image_bin = skimage.morphology.area_opening(image_bin)
        sum_each_row = np.sum(image_bin > 0, axis=1)
        xbounds = []
        bound = []
        for i, r in enumerate(sum_each_row):
            if (not bound) and r:  # start of bound
                bound.append(i)
            elif bound and (not r or i == len(sum_each_row) - 1):  # end of bound
                bound.append(i)
                xbounds.append(bound)
                bound = []
        xbounds = np.array(xbounds)
        image_decorated = image_orig.copy()
        boxes = []
        box = []
        for bound in xbounds:
            bound_upper, bound_lower = bound
            image_band = image_bin[bound_upper:bound_lower]
            sum_each_col = np.sum(image_band > 0, axis=0)
            for i, c in enumerate(sum_each_col):
                if (not box) and c:  # start of bound
                    box.extend([bound_upper, i])
                elif box and (not c or i == len(sum_each_col) - 1):  # end of bound
                    box.extend([bound_lower - bound_upper, i - box[-1]])
                    boxes.append(box)
                    box = []
        boxes = np.array(boxes)
        for box in boxes:
            image_decorated = draw_box(image_decorated, *box)

        pad = 5
        letters = []
        for box in boxes:
            xb, yb, hb, wb = box
            image_roi = image_bin[xb:xb+hb, yb:yb+wb]
            image_roi = cv2.copyMakeBorder(image_roi, pad, pad, pad, pad, cv2.BORDER_CONSTANT)
            image_roi = cv2.resize(image_roi, (32, 32), interpolation=cv2.INTER_CUBIC)
            image_roi = image_roi.astype("float32") / 255.0
            image_roi = np.expand_dims(image_roi, axis=-1)
            image_roi = image_roi.reshape(1, 32, 32, 1)
            ypred = self.__model.predict(image_roi, verbose=0)
            ypred = self.__LB.inverse_transform(ypred)
            [x] = self.__hex_to_char(ypred)
            letters.append(x)
        cv2.imwrite(str(analyzed_cell_directory + "/" + os.path.basename(img)), image_decorated)
        return letters
