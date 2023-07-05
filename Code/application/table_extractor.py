from pdf2image import convert_from_path
import cv2
import numpy as np
import file_manager as fm

global num_boxes, error

def pdf_to_jpg(file_path):
    global error
    error = False
    try:
        jpgs = convert_from_path(file_path)

        for page in range(len(jpgs)):
            jpgs[page].save('page' + str(page) + '.jpg', 'JPEG')
            return jpgs
    except:
        error = True
        return None
    

def rotate_jpgs(jpgs):
    imgs = []
    for page in range(len(jpgs)):
        img = cv2.imread('page' + str(page) + '.jpg')
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        imgs.append(img)
    return imgs

def prepare_binary_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_bin1 = 255-img_gray
    img_bin_otsu = cv2.threshold(img_bin1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    return img_bin_otsu

def get_vertical_lines(img_bin_otsu, img):
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, np.array(img).shape[1]//100))
    vertical_lines = cv2.erode(img_bin_otsu, vertical_kernel, iterations=3)
    vertical_lines = cv2.dilate(vertical_lines, vertical_kernel, iterations=3)
    return vertical_lines

def get_horizontal_lines(img_bin_otsu, img):
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (np.array(img).shape[1]//100, 1))
    horizontal_lines = cv2.erode(img_bin_otsu, horizontal_kernel, iterations=5)
    horizontal_lines = cv2.dilate(horizontal_lines, horizontal_kernel, iterations=5)
    return horizontal_lines

def get_vertical_horizontal_lines(vertical_lines, horizontal_lines):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 4))
    vertical_horizontal_lines = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    vertical_horizontal_lines = cv2.erode(~vertical_horizontal_lines, kernel, iterations=3)
    vertical_horizontal_lines = cv2.threshold(vertical_horizontal_lines, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    return vertical_horizontal_lines

def get_boundingBoxes(vertical_horizontal_lines):
    boundingBoxes = []
    contours = cv2.findContours(vertical_horizontal_lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]
    for contour in contours:
        boundingBox = cv2.boundingRect(contour)
        if ((boundingBox[2]<1000) and (boundingBox[3]<500)):
            boundingBoxes.append(boundingBox)
    return boundingBoxes

def sort_boundingBoxes(boundingBoxes):
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
    return boxes

def save_boxes(boxes, img):
    global num_boxes

    for box in boxes:
        x, y, w, h = box
        box_expand = 2
        roi = img[(y - box_expand):(y + h + box_expand), (x - box_expand):(x + w + box_expand)]
        filename = f'../../../../Storage/{num_boxes}.jpg'
        cv2.imwrite(filename, roi)
        num_boxes += 1
        
def extract_cells(file_path, messagebox):
    global num_boxes, error
    num_boxes = 0
    jpgs = pdf_to_jpg(file_path)
    if not error:
        imgs = rotate_jpgs(jpgs)
        for img in imgs:
            img_bin_otsu = prepare_binary_image(img)
            vertical_lines = get_vertical_lines(img_bin_otsu, img)
            horizontal_lines = get_horizontal_lines(img_bin_otsu, img)
            vertical_horizontal_lines = get_vertical_horizontal_lines(vertical_lines, horizontal_lines)
            boundingBoxes = get_boundingBoxes(vertical_horizontal_lines)
            boxes = sort_boundingBoxes(boundingBoxes)
            save_boxes(boxes, img)
        return 0
    else:
        messagebox()
        return -1
        
