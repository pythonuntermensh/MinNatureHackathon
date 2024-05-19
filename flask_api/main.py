from flask_cors import CORS
import zipfile
from zipfile import ZipFile
import io
from io import BytesIO
import pickle
import os
from flask import Flask, request, jsonify, send_file, make_response
import tensorflow
import numpy as np
import shutil
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from datetime import datetime
import glob


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
UPLOAD_MODEL_FOLDER = 'models'

files = os.listdir(os.path.join(BASE_DIR, UPLOAD_MODEL_FOLDER))

MODEL = load_model(UPLOAD_MODEL_FOLDER + "/" + "model.h5")


def predict(img_path, model):
    img = tensorflow.keras.preprocessing.image.load_img(img_path, target_size=(224,224))
    img_array = tensorflow.keras.preprocessing.image.img_to_array(img)
    expanded_img_array = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(expanded_img_array)
    prediction = model.predict(preprocessed_img)
    return prediction


def get_cropped_imgs(raw_imgs_path):
    os.popen("python " + os.path.join("yolov9", "detect.py") + " --weights " + os.path.join(UPLOAD_MODEL_FOLDER, "best.pt") + " \
  --img 640 --conf 0.6 --source " + os.path.join(UPLOAD_FOLDER, raw_imgs_path) + " --save-crop --name " + raw_imgs_path).read()
    
    cropped_files = glob.glob(os.path.join("yolov9", "runs", "detect", raw_imgs_path, "crops", "*", "*.*"), recursive=True)

    img_to_crops = {}
    raw_files = glob.glob(os.path.join(UPLOAD_FOLDER, raw_imgs_path, "*.*"))
    for file in raw_files:
        img_to_crops[file.split(os.path.sep)[-1]] = []
        for crop in cropped_files:
            _crop = ''.join(x for x in crop.split(os.path.sep)[-1].split(".")[:-1])
            _file = ''.join(x for x in file.split(os.path.sep)[-1].split(".")[:-1])
            if (_file.split("_____")[0] == _crop.split("_____")[0]):
                img_to_crops[file.split(os.path.sep)[-1]].append(crop)

    return img_to_crops


@app.route('/uploads_image', methods=['POST'])
def upload_images():
    if 'images' not in request.files:
        return jsonify({'error': 'netu nekogo'})
    images = request.files.getlist('images')
    dt_now = datetime.now().strftime("%d%b%Y-%H%M%S")
    os.mkdir(os.path.join(UPLOAD_FOLDER, dt_now))
    image_paths = []
    for image in images:
        filename = image.filename
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], dt_now, ''.join(x for x in filename.split(".")[:-1]) + "_____" + "." + filename.split(".")[-1])
        image.save(image_path)
        image_paths.append(image_path)

    imgs_to_crops = get_cropped_imgs(dt_now)
    classified_images = classify_images(imgs_to_crops)
    zip_path = create_archive(classified_images, dt_now)
    response = make_response(send_file(zip_path, as_attachment = True, download_name = f'results_{dt_now}.zip'))
    response.headers['Access-Control-Expose-Headers'] = "Content-Disposition"
    
    shutil.rmtree(os.path.join(UPLOAD_FOLDER, dt_now))
    shutil.rmtree(os.path.join("yolov9", "runs", "detect", dt_now))

    return response

@app.route('/classify', methods=['POST'])
def classify():
    if 'zip' not in request.files:
        return "No file part"
    
    file = request.files['zip']
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        dt_now = datetime.now().strftime("%d%b%Y-%H%M%S")
        with ZipFile(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as zip_ref:
            os.mkdir(os.path.join(UPLOAD_FOLDER, dt_now))
            zip_ref.extractall(os.path.join(app.config['UPLOAD_FOLDER'], dt_now))
            image_paths = [os.path.join(app.config['UPLOAD_FOLDER'], dt_now, f) for f in zip_ref.namelist()]
            print(image_paths)
            for image in image_paths:
                os.rename(image, os.path.join(UPLOAD_FOLDER, dt_now, ''.join(x for x in image.split(os.path.sep)[:-1]) + ''.join(x for x in image.split(os.path.sep)[-1].split(".")[:-1]) + "_____" + "." + image.split(os.path.sep)[-1].split(".")[-1]))
        
        imgs_to_crops = get_cropped_imgs(dt_now)
        classified_images = classify_images(imgs_to_crops)
        zip_path = create_archive(classified_images, dt_now)
        
        response = make_response(send_file(zip_path, as_attachment = True, download_name = f'results_{dt_now}.zip'))
        response.headers['Access-Control-Expose-Headers'] = "Content-Disposition"

        shutil.rmtree(os.path.join(app.config['UPLOAD_FOLDER'], dt_now))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        shutil.rmtree(os.path.join("yolov9", "runs", "detect", dt_now))

        return response

def create_archive(classified_images, metka):
    zip_path = os.path.join(app.config['UPLOAD_FOLDER'], 'classified_images.zip')
    with ZipFile(zip_path, 'w') as zipf:
        for class_name, images in classified_images.items():
            for image in images:
                image_filename = os.path.basename(image)
                zipf.write(os.path.join(UPLOAD_FOLDER, metka, image), arcname=os.path.join(class_name, image_filename.replace("_____", "")))
    return zip_path

def classify_images(imgs_to_crops):
    classes = {'Кабарги': [], 'Косули': [], 'Олени': []}
    for img, image_paths in imgs_to_crops.items():
        for image_path in image_paths:
            prediction = predict(image_path, MODEL)
            print(prediction)
            predicted_class = np.argmax(prediction)
            if(predicted_class == 0): predicted_class = 'Кабарги'
            elif(predicted_class == 1): predicted_class = 'Косули'
            else: predicted_class = 'Олени'
            classes[predicted_class].append(img)
    print(classes)
    return classes

if __name__ == '__main__':
    app.run(debug=True, port=8000)




