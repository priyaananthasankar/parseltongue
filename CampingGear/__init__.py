import logging

import azure.functions as func
from . import predict

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        req_body = req.get_json()
        urls = req_body.get('urls')
        results = predict.predict_gear(urls)
        return func.HttpResponse(results)
    except ValueError:
        pass
