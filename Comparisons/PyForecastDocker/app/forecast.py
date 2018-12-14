import logging
import io
from io import BytesIO
from io import StringIO
from pandas import Series
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error
from flask import Flask
from azure.storage.blob import ContentSettings
from azure.storage.blob import BlockBlobService
from flask import request

# Forecasting Algorithm using sklearn and statsmodels
# Reference: https://machinelearningmastery.com/autoregression-models-time-series-forecasting-python/

BLOB_NAME = "pncstorage101"
BLOB_KEY = ""
block_blob_service = BlockBlobService(account_name=BLOB_NAME, account_key=BLOB_KEY)
app = Flask(__name__)

def predict(series):

    # split dataset
    X = series.values
    train, test = X[1:len(X)-7], X[len(X)-7:]

    # train autoregression
    model = AR(train)
    model_fit = model.fit()
    logging.info('Lag: %s' % model_fit.k_ar)
    logging.info('Coefficients: %s' % model_fit.params)

    # make predictions
    predictions = model_fit.predict(start=len(train), end=len(train)+len(test)-1, dynamic=False)
    for i in range(len(predictions)):
	    logging.info('predicted=%f, expected=%f' % (predictions[i], test[i]))
    error = mean_squared_error(test, predictions)
    logging.info('Test MSE: %.3f' % error)
    # plot results
    pyplot.figure()
    pyplot.plot(test)
    pyplot.plot(predictions, color='red')

    # Save the plot as bytes
    buf = io.BytesIO()
    pyplot.savefig(buf,format="png")
    buf.seek(0)
    pyplotfile = buf.read()
    buf.close()
    return pyplotfile

@app.route("/api/ForecastAPI")
def forecast():
    dataset_name = request.args.get('name')
    result = request.args.get('result')
    generator = block_blob_service.list_blobs('forecastinput')
    for blob in generator:
        print("\t Blob name: " + blob.name)
    
    readblob = block_blob_service.get_blob_to_bytes("forecastinput", blob.name)
    data = StringIO(readblob.content.decode('utf-8'))
    series = Series.from_csv(data, header=0)
    result = predict(series)
    block_blob_service.create_blob_from_bytes("forecastoutput", "result.png", result)
    return "success"

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')        
