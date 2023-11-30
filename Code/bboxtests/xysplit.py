#!/usr/bin/env python

import sys

import skimage

sys.path.append("../tools")
sys.path.append("../application")
from bboxbenchmark import bboxbenchmark, get_metrics
from predict import predict
import cv2
import numpy as np


def show_img(img, title=None):
    title = title or ""
    cv2.imshow(title, img)
    if cv2.waitKey(0):
        cv2.destroyAllWindows()

def draw_box(src, x, y, h, w, r=0, g=200, b=0, a=0.4):
    overlay = src.copy()
    cv2.rectangle(overlay, (y, x), (y + w, x + h), (r, g, b),
                  -1)
    return cv2.addWeighted(overlay, a, src, 1 - a, 0)

class XYsplit(predict):
    @staticmethod
    def remove_lines(img):
        hkernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        hline = cv2.erode(img, hkernel, iterations=1)
        img = img - hline
        vkernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 25))
        vline = cv2.erode(img, vkernel, iterations=1)
        img = img - vline
        return img

    def _sort_bounding_boxes(self, bounding_boxes):
        sorted_bounding_boxes = sorted(bounding_boxes, key=lambda x: x[0])
        return sorted_bounding_boxes

    def get_letters(self, img, line_thickness):
        letters = []
        image_orig = cv2.imread(img)
        image_gray = cv2.cvtColor(image_orig, cv2.COLOR_BGR2GRAY)
        h, w = image_gray.shape
        _, image_bin = cv2.threshold(image_gray, 0, 255,
                                     cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        image_bin = cv2.erode(image_bin, np.ones((2, 2), np.uint8),
                              iterations=1)
        image_bin = cv2.dilate(image_bin, np.ones((3, 3), np.uint8),
                               iterations=1)
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
        # show_img(image_decorated)
        pad = 5
        letters = []
        for box in boxes:
            xb, yb, hb, wb = box
            image_roi = image_bin[xb:xb+hb, yb:yb+wb]
            image_roi = cv2.copyMakeBorder(image_roi, pad, pad, pad, pad, cv2.BORDER_CONSTANT)
            image_roi = cv2.resize(image_roi, (32, 32),
                                   interpolation=cv2.INTER_CUBIC)
            image_roi = image_roi.astype("float32") / 255.0
            image_roi = np.expand_dims(image_roi, axis=-1)
            image_roi = image_roi.reshape(1, 32, 32, 1)
            ypred = self._model.predict(image_roi, verbose=0)
            ypred = self._LB.inverse_transform(ypred)
            [x] = self._hex_to_char(ypred)
            letters.append(x)
        return letters

args = sys.argv[1:]
if not args:
    raise Exception("No directory given")
root_dir = args[0]
result_file = bboxbenchmark(XYsplit, root_dir)
get_metrics(root_dir + "/" + result_file)
