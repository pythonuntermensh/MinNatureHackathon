import customtkinter as ctk
from tkinter import filedialog, messagebox
import os
import tensorflow
import numpy as np
import shutil
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
import zipfile
from zipfile import ZipFile
import io
import pickle


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_MODEL_FOLDER = 'models'

files = os.listdir(os.path.join(BASE_DIR, UPLOAD_MODEL_FOLDER))

MODEL = load_model(UPLOAD_MODEL_FOLDER + "/" + "model.h5")

def update_classified_images(classified_images):
    updated_images = {}
    for key, value in classified_images.items():
        updated_images[key] = [item.split('\\')[-1] for item in value]
    return updated_images

def create_archive(classified_images):
    zip_path = filedialog.asksaveasfilename(
        title="Сохранить файл как",
        defaultextension=".zip",
        filetypes=[("Архивы", "*.zip;*.tar;*.tar.gz;*.tar.bz2"), ("Все файлы", "*.*")]
        )
    with ZipFile(zip_path, 'w') as zipf:
        for class_name, images in classified_images.items():
            for image in images:
                image_filename = os.path.basename(image)
                zipf.write(image, arcname=os.path.join(class_name, image_filename))
    return zip_path

def classify_images(image_paths):
    classes = {'Кабарги': [], 'Косули': [], 'Олени': []}
    for image_path in image_paths:
        predicted_class = np.argmax(predict(image_path, MODEL))
        if(predicted_class == 0): predicted_class = 'Кабарги'
        elif(predicted_class ==1): predicted_class = 'Косули'
        else: predicted_class = 'Олени'
        classes[predicted_class].append(image_path)
    return classes

def predict(img_path, model):
    img = tensorflow.keras.preprocessing.image.load_img(img_path, target_size=(224,224))
    img_array = tensorflow.keras.preprocessing.image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    prediction = model.predict(preprocessed_img)
    return prediction

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("SHA-256")
        self.geometry("300x300")

        self.select_photos_button = ctk.CTkButton(
            self, text="Выбрать фотографии", command=self.select_photos
        )
        self.select_photos_button.pack(pady=20)

        self.select_archive_button = ctk.CTkButton(
            self, text="Выбрать архив", command=self.select_archive
        )
        self.select_archive_button.pack(pady=20)

        self.UPLOAD_FOLDER = 'uploads'
        if not os.path.exists(self.UPLOAD_FOLDER):
            os.makedirs(self.UPLOAD_FOLDER)
            


    def select_photos(self):
        file_paths = filedialog.askopenfilenames(
            title="Выберите фотографии",
            filetypes=[("Файлы изображений", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
        )
        if file_paths:
            self.file_listbox.delete("1.0", ctk.END)
            for file_path in file_paths:
                self.file_listbox.insert(ctk.END, os.path.basename(file_path) + "\n")

    def select_archive(self):
        file = filedialog.askopenfilename(
            title="Выберите архив",
            filetypes=[("Архивы", "*.zip;*.tar;*.tar.gz;*.tar.bz2")],
        )
        if file:
            filename = file
            with ZipFile(os.path.join(self.UPLOAD_FOLDER, filename), 'r') as zip_ref:
                zip_ref.extractall(os.path.join(self.UPLOAD_FOLDER, 'temp'))
                image_paths = [os.path.join(self.UPLOAD_FOLDER, 'temp', f) for f in zip_ref.namelist()]
            classified_images = classify_images(image_paths)
            zip_path = create_archive(classified_images)
            messagebox.showinfo("Успешно", "Архив сформирован")
           # dict_str = "\n".join(f"{key}: {value}" for key, value in update_classified_images(classified_images).items())
           # messagebox.showinfo("Архив сформирован", dict_str)



if __name__ == "__main__":
    app = App()
    app.mainloop()
