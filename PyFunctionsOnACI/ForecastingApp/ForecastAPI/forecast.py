import logging
import io
from io import BytesIO
from pandas import Series
from matplotlib import pyplot
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error

# Forecasting Algorithm using sklearn and statsmodels
# Reference: https://machinelearningmastery.com/autoregression-models-time-series-forecasting-python/

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