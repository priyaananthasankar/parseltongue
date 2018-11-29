import logging

import azure.functions as func

import json
import os
import io
import time

# Imports for image processing
from PIL import Image

# Imports for prediction
import classify_image
import urllib
from urllib.request import urlopen 

def run_locally(image_url):
   results = classify_image.run_inference_on_image(image_url)

for i in range(0,50):
    start_time = time.time() 
    run_locally("test")
    print(time.time()-start_time)
