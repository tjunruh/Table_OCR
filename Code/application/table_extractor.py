from pdf2image import convert_from_path
import cv2
import numpy as np
import file_manager as fm

def extract_cells(file_path):
    jpgs = convert_from_path(file_path)

    for page in range(len(jpgs)):
        jpgs[page].save('page' + str(page) + '.jpg', 'JPEG')

    for page in range(len(jpgs)):
        img = cv2.imread('page' + str(page) + '.jpg')
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_bin1 = 255-img_gray
    thresh1, img_bin_otsu = cv2.threshold(img_bin1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 4))

    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, np.array(img).shape[1]//100))
    eroded_image = cv2.erode(img_bin_otsu, vertical_kernel, iterations=3)
    vertical_lines = cv2.dilate(eroded_image, vertical_kernel, iterations=3)

    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (np.array(img).shape[1]//100, 1))
    horizontal_lines = cv2.erode(img_bin_otsu, hor_kernel, iterations=5)

    horizontal_lines = cv2.dilate(horizontal_lines, hor_kernel, iterations=5)

    vertical_horizontal_lines = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    vertical_horizontal_lines = cv2.erode(~vertical_horizontal_lines, kernel, iterations=3)

    thresh, vertical_horizontal_lines = cv2.threshold(vertical_horizontal_lines, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(vertical_horizontal_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    boundingBoxes = []
    for contour in contours:
        boundingBox = cv2.boundingRect(contour)
        if ((boundingBox[2]<1000) and (boundingBox[3]<500)):
            boundingBoxes.append(boundingBox)
    rows_columns = []
    rows_columns = fm.load_rows_columns()
    columns = int(rows_columns[1])
    rows = int(len(boundingBoxes) / int(columns))
    boundingBoxes = sorted(boundingBoxes, key=lambda x:x[1])
    boxes = []
    for row in range(rows):
        start_position = (row*columns)
        grabbed_section = boundingBoxes[int(start_position):int(start_position + columns)]
        grabbed_section = sorted(grabbed_section, key=lambda x:x[0])
        boxes.extend(grabbed_section)
    

    for i, box in enumerate(boxes):

        x, y, w, h = box
        print(str(x) + " , " + str(y))
        box_expand = 2
        roi = img[(y - box_expand):(y + h + box_expand), (x - box_expand):(x + w + box_expand)]

        filename = f'../../Storage/box_{i}.jpg'
        cv2.imwrite(filename, roi)
    
    
