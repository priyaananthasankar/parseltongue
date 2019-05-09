import logging
import numpy as np
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    # Simple numpy operations
    a = np.triu(np.ones((3,3)),1) 
    logging.info(a)
    logging.info(a.T)
    return func.HttpResponse(f"Successfully used numpy operations")
