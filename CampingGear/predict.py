import logging
import azure.functions as func
import keras
from keras.models import load_model
import os
import pandas as pd
import numpy as np
from PIL import Image
from PIL import ImageOps
import json
import requests
import io
from io import BytesIO

classes = ['axes', 'boots', 'carabiners', 'crampons', 'gloves', 'hardshell jackets', 'harnesses', 'helmets', 'insulated jackets', 'pulleys', 'rope', 'tents']

def predict_gear(urls):
    model = load_model(os.path.join(os.getcwd(),"CampingGear","keras-gear.h5"))
    try:
        data = []
        for url in urls:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = process_images(img)
            img_arry = np.array(img)
            from keras import backend as K
            if K.image_data_format() == 'channels_first':
                print(img_arry.shape)
                img_arry = img_arry.reshape(1, 3, 128, 128)
                input_shape = (3, 128, 128)
            else:
                print(img_arry.shape)
                img_arry = img_arry.reshape(1, 128, 128, 3)
                input_shape = (128, 128, 3)

            img_arry = img_arry.astype('float32')
            img_arry /= 255
            prediction = model.predict_classes(img_arry).tolist()
            predict_name = classes[prediction[0]]
            data.append(predict_name)
        result = data
    except Exception as e:
        result = str(e)
    return json.dumps({"result": result})


def process_images(im):
    #Equalize the image
    converted_image = im.convert("RGB")
    equalizedim = ImageOps.equalize(converted_image)
    equalizedim.thumbnail((128,128))
    imsize = equalizedim.size

    #Set where the image needs to be pasted - top left corner of the pasted image
    leftCorner = (int((128-imsize[0])/2), int((128-imsize[1])/2))

    #create a new 128x128 box and paste the resized image in
    canvas = Image.new('RGB', (128,128), color=(255,255,255))
    canvas.paste(equalizedim, leftCorner)
    return canvas