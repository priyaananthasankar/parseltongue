import logging

import azure.functions as func

import json
import os
import io

# Imports for image processing
from PIL import Image

# Imports for prediction
from . import classify_image
import urllib
from urllib.request import urlopen

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
     
    image_url = req.params.get('img')

    results = classify_image.run_inference_on_image(image_url)
    
    logging.info(type(results))

    return json.dumps(results)