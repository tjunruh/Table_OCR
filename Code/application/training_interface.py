import tkinter as tk
from PIL import Image, ImageTk
from file_manager import file_manager
from training import training
import os

class training_interface:
    file_manager_operative = file_manager()
    training_operative = training()
    root = None
    __image_frame = None
    __approval_button_frame = None
    __approved_image_queue_frame = None
    __train_button_frame = None
    __train_output_frame = None
    __unapproved_image = None
    __image_label_container = None
    __approved_image_queue_label = None
    __train_output_label = None
    __image_path = None
    __image_label = None
    __image_label_display = None
    __approved_image_display = None
    __train_output_display = None


    def __get_image_name(self, path):
        image_num = os.path.basename(path)
        return image_num
        
    def __close(self):
        self.file_manager_operative.delete_discarded_training_images()
        self.__root.grab_release()
        self.__root.destroy()

    def __approve(self):
        self.file_manager_operative.mark_training_image_as_approved(self.__get_image_name(self.__image_path))
        self.__image_path, self.__image_label = self.file_manager_operative.load_unapproved_data()
        if self.__image_path != '':
            self.__unapproved_image = ImageTk.PhotoImage(Image.open(self.__image_path))
            self.__image_label_container.configure(image=self.__unapproved_image)
        else:
            self.__image_label_display.set("No Images Available")
            self.__image_label_container.configure(image='')
        
        self.__image_label_display.set(self.__image_label)
        number_of_approved_images = self.file_manager_operative.get_approved_data_quantity()
        self.__approved_image_display.set("Approved Data: " + str(number_of_approved_images))
        
    def __reject(self):
        self.file_manager_operative.mark_training_image_as_discarded(self.__get_image_name(self.__image_path))
        self.__image_path, self.__image_label = self.file_manager_operative.load_unapproved_data()
        if self.__image_path != '':
            self.__unapproved_image = ImageTk.PhotoImage(Image.open(self.__image_path))
            self.__image_label_container.configure(image=self.__unapproved_image)
        else:
            self.__image_label_display.set("No Images Available")
            self.__image_label_container.configure(image='')
            
        self.__image_label_display.set(self.__image_label)
        number_of_approved_images = self.file_manager_operative.get_approved_data_quantity()
        self.__approved_image_display.set("Approved Data: " + str(number_of_approved_images))
            
    
    def __train(self):
        if self.file_manager_operative.get_approved_data_quantity() > 0:
            self.__train_output_display.set("Training")
            self.training_operative.run_training()
            self.__train_output_display.set("Training Done")
            self.file_manager_operative.delete_approved_training_images()
            number_of_approved_images = self.file_manager_operative.get_approved_data_quantity()
            self.__approved_image_display.set("Approved Data: " + str(number_of_approved_images))
    
    def __load_images(self):
        image_paths = []
        images = []
        image_paths = self.file_manager_operative.load_unapproved_data()
        for path in image_paths:
            images.append(ImageTk.PhotoImage(Image.open(path)))
        return images

    def run(self):
        self.__root = tk.Toplevel()
        self.__root.grab_set()
        
        self.__root.title("Training")
        self.__root.rowconfigure(5, weight=1)
        self.__root.columnconfigure(1, weight=1)

        self.__image_frame = tk.Frame(self.__root)
        self.__image_frame.rowconfigure(0, weight=1)
        self.__image_frame.columnconfigure(0, weight=1)
        self.__image_frame.grid(row=0, column=0, sticky='nsew')

        self.__approval_button_frame = tk.Frame(self.__root)
        self.__approval_button_frame.rowconfigure(0, weight=1)
        self.__approval_button_frame.columnconfigure(1, weight=1)
        self.__approval_button_frame.grid(row=1, column=0, sticky='nsew')

        self.__approved_image_queue_frame = tk.Frame(self.__root)
        self.__approved_image_queue_frame.rowconfigure(0, weight=1)
        self.__approved_image_queue_frame.columnconfigure(0, weight=1)
        self.__approved_image_queue_frame.grid(row=2, column=0, sticky='nsew')

        self.__train_button_frame = tk.Frame(self.__root)
        self.__train_button_frame.rowconfigure(0, weight=1)
        self.__train_button_frame.columnconfigure(0, weight=1)
        self.__train_button_frame.grid(row=3, column=0, sticky='nsew')

        self.__train_output_frame = tk.Frame(self.__root)
        self.__train_output_frame.rowconfigure(0, weight=1)
        self.__train_output_frame.columnconfigure(0, weight=1)
        self.__train_output_frame.grid(row=4, column=0, sticky='nsew')


        self.__image_label_display = tk.StringVar(self.__root)
        self.__image_path, self.__image_label = self.file_manager_operative.load_unapproved_data()
        if self.__image_path != '':
            self.__unapproved_image = ImageTk.PhotoImage(Image.open(self.__image_path))
            self.__image_label_display.set(self.__image_label)
            self.__image_label_container = tk.Label(self.__image_frame, textvariable=self.__image_label_display, font=("Arial", 15), image=self.__unapproved_image, compound='top')
            self.__image_label_container.grid(row=0, column=0, sticky='nsew')
        else:
            self.__image_label_display.set("No New Images")
            self.__image_label_container = tk.Label(self.__image_frame, textvariable=self.__image_label_display, font=("Arial", 15))
            self.__image_label_container.grid(row=0, column=0, sticky='nsew')

        tk.Button(self.__approval_button_frame, text="Approve", font=("Arial", 15), command=self.__approve).grid(row=0, column=0, pady=10, padx=10)
        tk.Button(self.__approval_button_frame, text="Reject", font=("Arial", 15), command=self.__reject).grid(row=0, column=1, pady=10, padx=10)

        number_of_approved_images = self.file_manager_operative.get_approved_data_quantity()
        self.__approved_image_display = tk.StringVar(self.__root)
        self.__approved_image_display.set("Approved Data: " + str(number_of_approved_images))
        self.__approved_image_queue_label = tk.Label(self.__approved_image_queue_frame, textvariable=self.__approved_image_display, font=("Arial", 15))
        self.__approved_image_queue_label.grid(row=0, column=0, sticky='nsew')

        tk.Button(self.__train_button_frame, text="Train", font=("Arial", 15), comman=self.__train).grid(row=0, column=0, pady=10, padx=10)

        self.__train_output_display = tk.StringVar(self.__root)
        self.__train_output_display.set('')
        self.__train_output_label = tk.Label(self.__train_output_frame, textvariable=self.__train_output_display, font=("Arial", 15))
        self.__train_output_label.grid(row=0, column=0, sticky='nsew')

        self.__root.protocol("WM_DELETE_WINDOW", self.__close)
        self.__root.mainloop()      
