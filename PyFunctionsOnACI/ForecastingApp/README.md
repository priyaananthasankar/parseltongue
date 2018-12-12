# Time Series Forecasting using Python on Azure Functions

- This example demonstrates Azure Functions in Python deployed on an Azure Container Instance, that performs forecasting using scikit learn, statsmodel Python library. 

- It uses a Blob Storage input binding to read input and produce output and is triggered through HTTP.

Reference code:
https://machinelearningmastery.com/autoregression-models-time-series-forecasting-python/

# One Click Deploy to Azure

[![Deploy to Azure](http://azuredeploy.net/deploybutton.png)](https://azuredeploy.net/)

# Steps to develop

1. Fork this repository

2. Create a Python Virtual environment called "worker_env"
   
   `python3.6 -m venv worker_env`
   
3. Activate virtual environment
   
   `source worker_env/bin/activate`
   
4. Make modifications to suit your needs
    
    1. Change forecast.py to modify algorithms
    
    2. Change function.json and __init__.py to change triggers/bindings
    
5. Test your function
    
    1. Test locally first : `func host start`
    
    2. Build docker image from the root folder where Dockerfile is present
    
       Eg: `docker build --tag priya/forecast-app:v1 . `
       
    3. Test docker image
    
       Eg: `docker run -it -p 8080:80 priya/forecast-app:v1`
       
6. Publish to Azure Container Instance

    1. Create an Azure Storage Account and Blob Storage in your subscription. Create Blob containers called **forecastinput** and **forecastoutput**
    
    2. Upload **daily-minimum-temperatures.csv** file from the dataset folder in this repo into **forecastinput** folder.
    
    3. Click the Deploy to Azure Button in your fork (make sure you provide unique names to resource group/container DNS name)
    
       (or)
    
    4. Publish through Azure CLI by creating Azure Container Registry, pushing image and creating Azure Container Instance from the steps here:
    
       https://docs.microsoft.com/en-us/azure/container-instances/container-instances-tutorial-prepare-app
       
    5. Using a HTTP client call your function: 
    
       http://**{dnsname of your deployed container app}**/api/ForecastAPI?name=daily-minimum-temperatures.csv&result=result.png
    
    6. Check result.png graph in the forecastoutput container of your blob.