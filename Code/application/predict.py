import cv2
from file_manager import file_manager
import imutils
import numpy as np
from short_to_long import short_to_long
import time
import json
import requests
import os

class predict:
    file_manager_operative = file_manager()
    short_to_long_operative = short_to_long()
    __model = None
    __LB = None
    __error = None

    def __sort_contours(self, cnts, method="left-to-right"):
        reverse = False
        i = 0
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1
        boundingBoxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes), key=lambda b:b[1][i], reverse=reverse))

        return (cnts, boundingBoxes)

    def __get_letters(self, img, line_thickness):
        class_names = ['0', '1', '2', '3', '4', '5', '6',
                       '7', '8', '9', 'A', 'B', 'C', 'D',
                       'E', 'F', 'G', 'H', 'I', 'J', 'K',
                       'L', 'M', 'N', 'P', 'Q', 'R', 'S',
                       'T', 'U', 'V', 'W', 'X', 'Y']
        letters = []
        image = cv2.imread(img)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret,thresh1 = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
        dilated = cv2.dilate(thresh1, None, iterations=line_thickness)

        cnts = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        if len(cnts) > 0:
            cnts = self.__sort_contours(cnts, method="left-to-right")[0]

            box_expand = 2
            for c in cnts:
                if cv2.contourArea(c) > 125:
                    (x, y, w, h) = cv2.boundingRect(c)
                    cv2.rectangle(image, (x,y), (x+w,y+h), (0,255,0), 2)
                    roi = gray[(y - box_expand):(y + h + box_expand), (x - box_expand):(x + w + box_expand)]
                    thresh = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                    try:
                        thresh = cv2.resize(thresh, (32, 32), interpolation = cv2.INTER_CUBIC)
                        thresh = thresh.astype("float32") / 255.0
                        thresh = np.expand_dims(thresh, axis=-1)
                        thresh = thresh.reshape(1,32,32,1)
                        data = json.dumps({"signature_name": "serving_default", "instances": thresh.tolist()})
                        headers = {"content-type": "application/json"}
                        json_response = requests.post('http://localhost:8501/v1/models/Table_OCR_model:predict', data=data, headers=headers)
                        ypred = json.loads(json_response.text)['predictions']
                        ypred = class_names[np.argmax(ypred[0])]
                        letters.append(ypred)
                    except:
                        self.__error = True
            return letters

    def __get_word(self, letters):
        word = ""
        if letters:
            for letter in letters:
                word += letter
        return word

    def get_predictions(self, root, pb, messagebox, line_thickness, find_shorthand_matches):
        global model, LB, error
        self.__error = False
        predictions = []
        self.file_manager_operative.delete_ignored_rows()
        cells = self.file_manager_operative.get_storage()
        job_length = len(cells)
        job_num = 0
        default_word = ''
        for cell in cells:
            if find_shorthand_matches == 1:
                for boldness in range(2,5):
                    letters = self.__get_letters(cell, boldness)
                    if self.__error:
                        break
                    word = self.__get_word(letters)
                    if boldness == line_thickness:
                        default_word = word
                    if self.short_to_long_operative.in_short(word):
                        break
                    else:
                        word = default_word 
            else:
                letters = self.__get_letters(cell, line_thickness)
                word = self.__get_word(letters)

            if self.__error:
                self.__error = False
                predictions.clear()
                messagebox()
                break
            
            predictions.append(word)
            pb['value'] = int((job_num / job_length) * 100)
            job_num += 1
            root.update_idletasks()
        pb['value'] = 100
        root.update_idletasks()
        time.sleep(1)
        pb['value'] = 0
        root.update_idletasks()

        predictions = self.short_to_long_operative.short_to_long(predictions)

        return predictions
