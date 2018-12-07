import logging
import os
import json
import azure.functions as func
from . import forecast
from pandas import Series
from io import StringIO

def main(req: func.HttpRequest,
         input: func.InputStream,
         output: func.Out[bytes]) -> func.HttpResponse:
    
    logging.info('Python HTTP trigger function processed a request.')

    # If data has to be read from local csv file, you can mention the path this way
    # path = os.path.join(os.getcwd(),"ForecastAPI","daily-minimum-temperatures.csv")
    # Else, you can read it as a string from the blob and feed into from_csv this way,
    # This is more stateless and ready for operationalizing this ML flow.

    data = StringIO(input.read().decode('utf-8'))
    series = Series.from_csv(data, header=0)
    result = forecast.predict(series)
    output.set(result)

    return func.HttpResponse("Success")