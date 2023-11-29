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


class BtrMorph(predict):
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
        _, image_bin = cv2.threshold(image_gray, 0, 255,
                                     cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        image_bin = cv2.erode(image_bin, np.ones((2, 2), np.uint8),
                              iterations=1)
        image_bin = cv2.dilate(image_bin, np.ones((3, 3), np.uint8),
                               iterations=2)
        image_bin = skimage.morphology.area_opening(image_bin)
        bounding_boxes = []
        analysis = cv2.connectedComponentsWithStats(image_bin, 4, cv2.CV_32S)
        (totalLabels, label_ids, values, centroid) = analysis
        # Loop through each component
        new_img = image_orig.copy()
        for i in range(1, totalLabels):

            # Area of the component
            area = values[i, cv2.CC_STAT_AREA]

            # Now extract the coordinate points
            x1 = values[i, cv2.CC_STAT_LEFT]
            y1 = values[i, cv2.CC_STAT_TOP]
            w = values[i, cv2.CC_STAT_WIDTH]
            h = values[i, cv2.CC_STAT_HEIGHT]

            bounding_boxes.append([x1, y1, w, h])

            # Coordinate of the bounding box
            pt1 = (x1, y1)
            pt2 = (x1 + w, y1 + h)

            # Bounding boxes for each component
            cv2.rectangle(new_img, pt1, pt2, (0, 255, 0), 3)
        # show_img(new_img)
        if len(bounding_boxes) > 0:
            bounding_boxes = self._sort_bounding_boxes(bounding_boxes)
            box_expand = 2
            for box in bounding_boxes:
                (x, y, w, h) = box
                roi = image_gray[(y - box_expand):(y + h + box_expand),
                      (x - box_expand):(x + w + box_expand)]
                image_bin = cv2.threshold(roi, 0, 255,
                                          cv2.THRESH_BINARY_INV |
                                          cv2.THRESH_OTSU)[
                    1]
                try:
                    image_bin = cv2.resize(image_bin, (32, 32),
                                           interpolation=cv2.INTER_CUBIC)
                    image_bin = image_bin.astype("float32") / 255.0
                    image_bin = np.expand_dims(image_bin, axis=-1)
                    image_bin = image_bin.reshape(1, 32, 32, 1)
                    ypred = self._model.predict(image_bin, verbose=0)
                    ypred = self._LB.inverse_transform(ypred)
                    [x] = self._hex_to_char(ypred)
                    letters.append(x)
                except Exception as e:
                    pass

            return letters


args = sys.argv[1:]
if not args:
    raise Exception("No directory given")
root_dir = args[0]
result_file = bboxbenchmark(BtrMorph, root_dir)
get_metrics(root_dir + "/" + result_file)
