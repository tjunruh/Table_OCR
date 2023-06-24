from pdf2image import convert_from_path
import cv2
import numpy as np

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

    thresh, vertical_horizontal_lines = cv2.threshold(vertical_horizontal_lines, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    contours, hierarchy = cv2.findContours(vertical_horizontal_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    boundingBoxes = [cv2.boundingRect(contour) for contour in contours]
    (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), key=lambda x:x[1][1], reverse=False))

    boxes = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if (w<1000 and h<500):
            image = cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            boxes.append([x,y,w,h])

    for i, box in enumerate(boxes):

        x, y, w, h = box
        box_expand = 2
        roi = img[(y - box_expand):(y + h + box_expand), (x - box_expand):(x + w + box_expand)]

        filename = f'../../Storage/box_{i}.jpg'
        cv2.imwrite(filename, roi)
    
    
