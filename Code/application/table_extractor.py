from pdf2image import convert_from_path
import cv2
import numpy as np
from file_manager import file_manager

class table_extractor:
    file_manager_operative = file_manager()
    __num_boxes = None
    __convert_pdf_error = None
    __number_of_cells_error = None

    def __pdf_to_jpg(self, file_path):
        self.__convert_pdf_error = False
        try:
            jpgs = convert_from_path(file_path, poppler_path='../../Release-23.07.0-0/poppler-23.07.0/Library/bin')

            for page in range(len(jpgs)):
                jpgs[page].save('page' + str(page) + '.jpg', 'JPEG')

            return jpgs
        except:
            self.__convert_pdf_error = True
            return None
    

    def __rotate_jpgs(self, jpgs):
        imgs = []
        for page in range(len(jpgs)):
            img = cv2.imread('page' + str(page) + '.jpg')
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            imgs.append(img)
        return imgs

    def __prepare_binary_image(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_bin1 = 255-img_gray
        img_bin_otsu = cv2.threshold(img_bin1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return img_bin_otsu

    def __get_vertical_lines(self, img_bin_otsu, img):
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, np.array(img).shape[1]//100))
        vertical_lines = cv2.erode(img_bin_otsu, vertical_kernel, iterations=3)
        vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=3)
        return vertical_lines

    def __get_horizontal_lines(self, img_bin_otsu, img):
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (np.array(img).shape[1]//100, 1))
        horizontal_lines = cv2.erode(img_bin_otsu, horizontal_kernel, iterations=5)
        horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=5)
        return horizontal_lines

    def __get_vertical_horizontal_lines(self, vertical_lines, horizontal_lines):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 4))
        vertical_horizontal_lines = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        vertical_horizontal_lines = cv2.erode(~vertical_horizontal_lines, kernel, iterations=3)
        vertical_horizontal_lines = cv2.threshold(vertical_horizontal_lines, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return vertical_horizontal_lines

    def __get_boundingBoxes(self, vertical_horizontal_lines):
        boundingBoxes = []
        contours = cv2.findContours(vertical_horizontal_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        for contour in contours:
            boundingBox = cv2.boundingRect(contour)
            if ((boundingBox[2]<1000) and (boundingBox[3]<500) and (boundingBox[2]>25) and (boundingBox[3]>25)):
                boundingBoxes.append(boundingBox)
        return boundingBoxes

    def __sort_boundingBoxes(self, boundingBoxes):
        self.__number_of_cells_error = False
        rows_columns = []
        rows_columns = self.file_manager_operative.load_rows_columns()
        if(int(rows_columns[0])*int(rows_columns[1]) != int(len(boundingBoxes))):
           self.__number_of_cells_error = True
           return None
        columns = int(rows_columns[1])
        rows = int(len(boundingBoxes) / int(columns))
        boundingBoxes = sorted(boundingBoxes, key=lambda x:x[1])
        boxes = []
        for row in range(rows):
            start_position = (row*columns)
            grabbed_section = boundingBoxes[int(start_position):int(start_position + columns)]
            grabbed_section = sorted(grabbed_section, key=lambda x:x[0])
            boxes.extend(grabbed_section)
        return boxes

    def __save_boxes(self, boxes, img):
        for box in boxes:
            x, y, w, h = box
            box_expand = 2
            roi = img[(y - box_expand):(y + h + box_expand), (x - box_expand):(x + w + box_expand)]
            filename = f'../../Storage/{self.__num_boxes}.jpg'
            cv2.imwrite(filename, roi)
            self.__num_boxes += 1
        
    def extract_cells(self, file_path, messagebox_pdf_error, messagebox_number_of_cells_error):
        self.__num_boxes = 0
        jpgs = self.__pdf_to_jpg(file_path)
        if not self.__convert_pdf_error:
            imgs = self.__rotate_jpgs(jpgs)
            for img in imgs:
                img_bin_otsu = self.__prepare_binary_image(img)
                vertical_lines = self.__get_vertical_lines(img_bin_otsu, img)
                horizontal_lines = self.__get_horizontal_lines(img_bin_otsu, img)
                vertical_horizontal_lines = self.__get_vertical_horizontal_lines(vertical_lines, horizontal_lines)
                boundingBoxes = self.__get_boundingBoxes(vertical_horizontal_lines)
                boxes = self.__sort_boundingBoxes(boundingBoxes)
                if(self.__number_of_cells_error):
                   messagebox_number_of_cells_error()
                   return -1
                self.__save_boxes(boxes, img)
            return 0
        else:
            messagebox_pdf_error()
            return -1
        
