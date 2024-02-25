#!/usr/bin/env python3

import sys

sys.path.append("../tools")
sys.path.append("../application")
from file_manager import file_manager
import cv2
import numpy as np
import os
import time

class ConnCompBtrMorph:
    file_manager_operative = file_manager()
    __model = None
    __LB = None

    def __init__(self):
        self.__LB = self.file_manager_operative.load_LabelBinarizer()
        self.__model = self.file_manager_operative.load_ocr_model()

    def __hex_to_char(self, hex_input):
        return(chr(int(hex_input[0], 16)))

    def __sort_bounding_boxes(self, bounding_boxes):
        sorted_bounding_boxes = sorted(bounding_boxes, key=lambda x: x[0])
        return sorted_bounding_boxes

    def __check_node_connections(self, node, components, grouped_components, analyzed_component_ids, x_tolerance, y_tolerance):
        node_bounding_box, node_centroid = node
        index = 0
        for component in components:
            if index not in analyzed_component_ids:
                bounding_box, centroid = component
                x_node, y_node = node_centroid
                x_component, y_component = centroid
                if (abs(x_node - x_component) < x_tolerance) and (abs(y_node - y_component) < y_tolerance):
                    grouped_components.append(component)
                    analyzed_component_ids.append(index)
                    grouped_components, analyzed_component_ids = self.__check_node_connections(component, components, grouped_components, analyzed_component_ids, x_tolerance, y_tolerance)
            index = index + 1

        return grouped_components, analyzed_component_ids
        
    def __group_components(self, bounding_boxes, centroids, x_tolerance, y_tolerance):
        updated_components = []
        component_subgroup = []
        analyzed_component_ids = []
        index = 0
        components = tuple(zip(bounding_boxes, centroids))
        for component in components:
            if index not in analyzed_component_ids:
                component_subgroup.append(component)
                analyzed_component_ids.append(index)
                component_subgroup, analyzed_component_ids = self.__check_node_connections(component, components, component_subgroup, analyzed_component_ids, x_tolerance, y_tolerance)
                updated_components.append(component_subgroup)
                component_subgroup = []
            index = index + 1
        return updated_components

    def __multiple_lines(self, centroids, y_tolerance):
        y_points = []
        multiple_lines = False
        for x, y in centroids:
            y_points.append(y)
        if (max(y_points) - min(y_points)) > y_tolerance:
            multiple_lines = True
        return multiple_lines

    def __merge_groups(self, grouped_components):  
        x1_group = []
        x2_group = []
        y1_group = []
        y2_group = []
        centroid_group = []
        updated_bounding_boxes = []
        updated_centroids = []
        for subgroup in grouped_components:
            for bounding_box, centroid in subgroup:
                x1, y1, x2, y2 = bounding_box
                x1_group.append(x1)
                x2_group.append(x2)
                y1_group.append(y1)
                y2_group.append(y2)
            x1 = min(x1_group)
            x2 = max(x2_group)
            y1 = min(y1_group)
            y2 = max(y2_group)
            updated_bounding_boxes.append([x1, y1, x2, y2])
            updated_centroids.append([int(x1 + ((x2 - x1)/2)), int(y1 + ((y2 - y1)/2))])
            x1_group = []
            x2_group = []
            y1_group = []
            y2_group = []
        return updated_bounding_boxes, updated_centroids

    def __separate_groups(self, grouped_components):
        updated_bounding_boxes = []
        updated_bounding_boxes_subgroup = []
        i = 0
        for subgroup in grouped_components:
            if i > 0:
                updated_bounding_boxes.append(',')
            for bounding_box, centroid in subgroup:
                updated_bounding_boxes_subgroup.append(bounding_box)
            updated_bounding_boxes_subgroup = self.__sort_bounding_boxes(updated_bounding_boxes_subgroup)
            updated_bounding_boxes.extend(updated_bounding_boxes_subgroup)
            updated_bounding_boxes_subgroup = []
            i = i + 1
        return updated_bounding_boxes
        
    def get_letters(self, img, analyzed_cell_directory):
        x_tolerance = 20
        y_tolerance = 30
        letters = []
        image_orig = cv2.imread(img)
        image_gray = cv2.cvtColor(image_orig, cv2.COLOR_BGR2GRAY)
        threshold_level, image_bin = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        if threshold_level > 225:
            threshold_level, image_bin = cv2.threshold(image_gray, 225, 255, cv2.THRESH_BINARY_INV)
        image_bin = cv2.erode(image_bin, np.ones((2, 2), np.uint8), iterations=1)
        image_bin = cv2.dilate(image_bin, np.ones((3, 3), np.uint8), iterations=1)
        bounding_boxes = []
        centroids = []
        analysis = cv2.connectedComponentsWithStats(image_bin, 4, cv2.CV_32S)
        (totalLabels, label_ids, values, centroid) = analysis
        
        # Loop through each component
        new_img = image_orig.copy()
        for i in range(1, totalLabels):

            # Area of the component
            area = values[i, cv2.CC_STAT_AREA]
            if (area > 65):
                # Now extract the coordinate points
                x1 = values[i, cv2.CC_STAT_LEFT]
                y1 = values[i, cv2.CC_STAT_TOP]
                w = values[i, cv2.CC_STAT_WIDTH]
                h = values[i, cv2.CC_STAT_HEIGHT]

                x2 = x1 + w
                y2 = y1 + h
                xc, yc = centroid[i]
                bounding_boxes.append([x1, y1, x2, y2])
                centroids.append([xc, yc])

        if len(bounding_boxes) > 0:
            grouped_components = self.__group_components(bounding_boxes, centroids, x_tolerance, y_tolerance)
            bounding_boxes, centroids = self.__merge_groups(grouped_components)
            if self.__multiple_lines(centroids, 25):
                grouped_components = self.__group_components(bounding_boxes, centroids, 2000, 25)
                bounding_boxes = self.__separate_groups(grouped_components)
            else:
                bounding_boxes = self.__sort_bounding_boxes(bounding_boxes)
            box_expand = 5
            i = 0
            while i < len(bounding_boxes):
                if bounding_boxes[i] != ',':
                    (x1, y1, x2, y2) = bounding_boxes[i]
                    x1_adjusted = x1 - box_expand
                    y1_adjusted = y1 - box_expand
                    x2_adjusted = x2 + box_expand
                    y2_adjusted = y2 + box_expand
                    cv2.rectangle(new_img, [x1_adjusted, y1_adjusted], [x2_adjusted, y2_adjusted], (0, 255, 0), 3)
                    roi = image_gray[y1_adjusted:y2_adjusted, x1_adjusted:x2_adjusted]
                    image_bin = cv2.threshold(roi, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
                    try:
                        image_bin = cv2.resize(image_bin, (32, 32), interpolation=cv2.INTER_CUBIC)
                        image_bin = image_bin.astype("float32") / 255.0
                        image_bin = np.expand_dims(image_bin, axis=-1)
                        image_bin = image_bin.reshape(1, 32, 32, 1)
                        ypred = self.__model.predict(image_bin, verbose=0)
                        ypred = self.__LB.inverse_transform(ypred)
                        [x] = self.__hex_to_char(ypred)
                        letters.append(x)
                        bounding_boxes[i] = (x1_adjusted, y1_adjusted, x2_adjusted, y2_adjusted)
                        i = i + 1
                        box_expand = 5
                    except Exception as e:
                        if box_expand > 0:
                            box_expand = box_expand - 1
                        else:
                            i = i + 1
                else:
                    letters.append(',')
                    i = i + 1
        cv2.imwrite(str(analyzed_cell_directory + "/" + os.path.basename(img)), new_img)
        return letters

