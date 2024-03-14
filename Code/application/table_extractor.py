from pdf2image import convert_from_path
import cv2
import numpy as np
from file_manager import file_manager

class table_extractor:
    file_manager_operative = file_manager()
    __num_boxes = None
    __convert_pdf_error = None
    __number_of_cells_error = None
    __measured_cell_number = None
    __number_of_pages = None

    def __pdf_to_jpg(self, file_path):
        self.__convert_pdf_error = False
        try:
            jpgs = convert_from_path(file_path, poppler_path=self.file_manager_operative.poppler_path) 

            for page in range(len(jpgs)):
                jpgs[page].save(
                    self.file_manager_operative.raw_page_path / f"page{page}.jpg",
                    'JPEG')

            return jpgs
        except:
            self.__convert_pdf_error = True
            return None
    

    def __rotate_jpgs(self, jpgs):
        imgs = []
        for page in range(len(jpgs)):
            img = cv2.imread(
                str(self.file_manager_operative.raw_page_path / f"page{page}.jpg")
            )
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            imgs.append(img)
        return imgs

    def __prepare_binary_image(self, img):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img_bin1 = 255-img_gray
        img_bin_otsu = cv2.threshold(img_bin1, 25, 255, cv2.THRESH_BINARY)[1]
        
        analysis = cv2.connectedComponentsWithStats(img_bin_otsu, 4, cv2.CV_32S)
        (totalLabels, label_ids, values, centroid) = analysis

        sizes = values[:, cv2.CC_STAT_AREA]
        max_label = 1
        max_size = sizes[1]
        for i in range(2, totalLabels):
            if sizes[i] > max_size:
                max_label = i
                max_size = sizes[i]
        extracted_table = (label_ids == max_label).astype("uint8") * 255
        return extracted_table

    def __get_vertical_lines(self, img_bin_otsu, img):
        vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, np.array(img).shape[1]//225))
        vertical_lines = cv2.erode(img_bin_otsu, vertical_kernel, iterations=3)
        vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=5)
        return vertical_lines

    def __get_horizontal_lines(self, img_bin_otsu, img):
        horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (np.array(img).shape[1]//225, 1))
        horizontal_lines = cv2.erode(img_bin_otsu, horizontal_kernel, iterations=3)
        horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=5)
        return horizontal_lines

    def __get_vertical_horizontal_lines(self, vertical_lines, horizontal_lines):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 4))
        vertical_horizontal_lines = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        vertical_horizontal_lines = cv2.dilate(vertical_horizontal_lines, kernel, iterations=3)
        vertical_horizontal_lines = cv2.threshold(vertical_horizontal_lines, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        return vertical_horizontal_lines

    def __get_boundingBoxes(self, vertical_horizontal_lines):
        boundingBoxes = []
        contours = cv2.findContours(vertical_horizontal_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
        for contour in contours:
            boundingBox = cv2.boundingRect(contour)
            if ((boundingBox[2]<1000) and (boundingBox[3]<500) and (boundingBox[2]>25) and (boundingBox[3]>25)):
                boundingBoxes.append(boundingBox)
        self.__measured_cell_number = self.__measured_cell_number + len(boundingBoxes)
        return boundingBoxes

    def __sort_boundingBoxes(self, boundingBoxes):
        self.__number_of_cells_error = False
        rows_columns = []
        rows_columns = self.file_manager_operative.load_rows_columns()
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

    def __remove_ignored_rows(self, boxes):
        ignore = []
        ignore = self.file_manager_operative.load_ignore()
        rows_columns = []
        rows_columns = self.file_manager_operative.load_rows_columns()
        for page, row in ignore:
            start_cell = (int(page) - 1)*int(rows_columns[0])*int(rows_columns[1]) + (int(row) - 1)*int(rows_columns[1])
            stop_cell = start_cell + int(rows_columns[1])
            self.__remove_ignored_rows_in_range(boxes, start_cell, stop_cell)
        return boxes

    def __remove_ignored_rows_in_range(self, boxes, start_cell, stop_cell):
        del boxes[start_cell:stop_cell]
        return boxes

    def __save_boxes(self, boxes, img):
        for box in boxes:
            x, y, w, h = box
            roi = img[y:(y + h), x:(x + w)]
            self.file_manager_operative.save_raw_storage_single(roi, self.__num_boxes)
            self.__num_boxes += 1

    def get_measured_cell_number(self):
        return self.__measured_cell_number

    def get_number_of_pages(self):
        return self.__number_of_pages
        
    def extract_cells(self, file_path):
        self.__measured_cell_number = 0
        self.__number_of_pages = 0
        self.__num_boxes = 0
        self.file_manager_operative.clear_raw_page()
        self.file_manager_operative.clear_processed_page()
        jpgs = self.__pdf_to_jpg(file_path)
        if not self.__convert_pdf_error:
            imgs = self.__rotate_jpgs(jpgs)
            self.__number_of_pages = len(imgs)
            for img in range(len(imgs)):
                img_bin_otsu = self.__prepare_binary_image(imgs[img])
                vertical_lines = self.__get_vertical_lines(img_bin_otsu, imgs[img])
                horizontal_lines = self.__get_horizontal_lines(img_bin_otsu, imgs[img])
                vertical_horizontal_lines = self.__get_vertical_horizontal_lines(vertical_lines, horizontal_lines)
                vertical_horizontal_lines = ~vertical_horizontal_lines
                self.file_manager_operative.save_processed_page_single(vertical_horizontal_lines, img)
                boundingBoxes = self.__get_boundingBoxes(vertical_horizontal_lines)
                boxes = self.__sort_boundingBoxes(boundingBoxes)
                boxes = self.__remove_ignored_rows(boxes)
                self.__save_boxes(boxes, imgs[img])
            return 0
        else:
            return -1
        
