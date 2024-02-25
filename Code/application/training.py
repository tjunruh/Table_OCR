from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
from file_manager import file_manager
import cv2
import numpy as np
import sys

class training:
    file_manager_operative = file_manager()
    __image_size = 32

    def char_to_hex(self, char):
        return hex(ord(char)).replace('0x', '')

    def get_data(self):
        image_paths = []
        image_labels = []
        image_bounding_boxes = []
        image_paths, image_labels, image_bounding_boxes = self.file_manager_operative.load_approved_data()
        cells = []
        for path in image_paths:
            image = cv2.imread(path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cells.append(image)
        characters = []
        j = 0
        for i in range(len(image_bounding_boxes)):
            cell = cells[i]
            for box in image_bounding_boxes[i]:
                x1, y1, x2, y2 = box
                character = cell[y1:y2, x1:x2]
                character = cv2.resize(character, (self.__image_size, self.__image_size), interpolation=cv2.INTER_CUBIC)
                j = j + 1
                self.file_manager_operative.save_training_image_output_image(character, str(j) + '.jpg')
                characters.append(character)
        character_labels = []
        for label in image_labels:
            for char in label:
                character_labels.append(self.char_to_hex(char))
        LB = self.file_manager_operative.load_LabelBinarizer()
        character_labels = LB.transform(character_labels)
        train_x = []
        train_x = np.array(characters)/255.0
        train_x = train_x.reshape(len(characters), self.__image_size, self.__image_size, 1)
        train_y = np.array(character_labels)
        return train_x, train_y
        

    def run_training(self):
        self.file_manager_operative.clear_training_output()
        train_x, train_y = self.get_data()
        model = self.file_manager_operative.load_ocr_model()
        epochs = 100
        variable = ReduceLROnPlateau(monitor='loss', factor = 0.2, patience = 10)
        early_stop = EarlyStopping(monitor='loss', patience = 15)
        with open(str(self.file_manager_operative.training_output_path / "output.txt"), 'w') as sys.stdout:
            history = model.fit(train_x, train_y, epochs = epochs, callbacks=[early_stop, variable])
        self.file_manager_operative.save_ocr_model(model)
        
        
        
        
        
            
