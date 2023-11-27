import tensorflow as tf
import cv2
from file_manager import file_manager
from sklearn.preprocessing import LabelBinarizer
import imutils
import numpy as np
from short_to_long import short_to_long
import time
from multiprocessing import Pool, cpu_count, Value

class predict:
    file_manager_operative = file_manager()
    short_to_long_operative = short_to_long()
    __model = None
    __LB = None

    def __init__(self):
        self.__LB = self.file_manager_operative.load_LabelBinarizer()
        self.__model = self.file_manager_operative.load_ocr_model()

    def __hex_to_char(self, hex_input):
        return(chr(int(hex_input[0], 16)))

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

    def get_letters(self, img, line_thickness):
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
                        ypred = self.__model.predict(thresh, verbose=0)
                        ypred = self.__LB.inverse_transform(ypred)
                        [x] = self.__hex_to_char(ypred)
                        letters.append(x)
                    except Exception as e:
                        pass
                    
            return letters

    def __get_word(self, letters):
        word = ""
        if letters:
            for letter in letters:
                word += letter
        return word

    def get_predictions(self, cells, line_thickness, find_shorthand_matches, multiprocessing):
        global m_job_num
        predictions = []
        default_word = ''
        for cell in cells:
            if find_shorthand_matches == 1:
                for boldness in range(2,5):
                    letters = self.get_letters(cell, boldness)
                    word = self.__get_word(letters)
                    if boldness == line_thickness:
                        default_word = word
                        
                    if self.short_to_long_operative.in_short(word):
                        break
                    else:
                        word = default_word 
            else:
                letters = self.get_letters(cell, line_thickness)
                word = self.__get_word(letters)
            
            predictions.append(word)
            if multiprocessing:
                m_job_num.value += 1

        predictions = self.short_to_long_operative.short_to_long(predictions)
        return predictions

    def run_batch_predictions(self, batch_num):
        cells = self.file_manager_operative.load_batch(batch_num)
        line_thickness = self.file_manager_operative.load_line_thickness()
        find_shorthand_matches = self.file_manager_operative.load_find_shorthand_matches()
        predictions = self.get_predictions(cells, int(line_thickness), int(find_shorthand_matches), True)
        self.file_manager_operative.save_prediction_results(predictions, batch_num)

    def init_workers(self, job_num):
        global m_job_num
        m_job_num = job_num

    def update_progress_bar(self, job_num, job_len, pb, root):
        while(job_num.value < (job_len - 1)):
            pb['value'] = int((job_num.value / job_len) * 100)
            root.update_idletasks()
            time.sleep(0.25)
        pb['value'] = 100
        time.sleep(0.25)
        pb['value'] = 0

    def run_predictions(self, cells_len, pb, root):
        __name__ = '__main__'
        if __name__ == '__main__':
            job_num = Value('i', 0)
            cpu_num = int(cpu_count()/2)
            p1 = Pool(cpu_num, initializer=self.init_workers, initargs=(job_num,))
            p1.map_async(self.run_batch_predictions, range(1, cpu_num+1))
            p1.close()
            self.update_progress_bar(job_num, cells_len, pb, root)
            p1.join()
        
