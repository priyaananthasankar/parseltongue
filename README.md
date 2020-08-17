# Python on Azure Functions

## Status: GA : Please refer official documentation [here](https://docs.microsoft.com/en-us/azure/azure-functions/functions-reference-python)
* Exploring Functions on AKS to use GPU's https://medium.com/@asavaritayal/azure-functions-on-kubernetes-75486225dac0 

You can explore this repository but all of these samples are now moved officially into Azure Samples - Please refer official documentation. 

# Machine Learning with Functions

## Sample 1 : Topic Modeling using Gensim

This sample demonstrates LDA topic modeling of Gutenberg books using Gensim/NLTK/Azure Python Storage SDK/ PyLDAVis Python libraries.

### Try it out!

curl -X POST -H 'Content-Type:application/json' -d '{ "container_name" : "janeausten", "num_topics" : 20 }' https://gutenbergery.azurewebsites.net/api/TrainBookcode=mhu/Ihigx/0wgEtuyRybGDXRSah0vJ3wdsGT7rd2MMuuZOMCPFauqw==https://gutenbergbooks.blob.core.windows.net/janeaustenmodels/ldamodel.html

Performs the following tasks:

* On HttpTrigger, loads dataset from blob, cleans dataset (removes newlines and carriage returns etc)
* Sentence tokenizes it and removes stopwords (NLTK)
* Builds a dictionary using this data and feeds it to Gensim for topic modeling
* Runs 15 passes of modeling , num_topics we need is 20 (this is just a human readable number)
* Uses the model, dictionary, corpus and visualizes topics using PyLDAVis
* Supposed to lemmatize the words (see Gaps/Issues below)
* Outputs the visualized HTML (PyLDAVIS)

## Sample 2 : Inferencing from Keras

Performs the following

Loads a pretrained Keras model from a local function app zip blob.
Accepts image URL's and uses Keras model for inferencing. Takes in URL's of images that show camping gear, uses Keras model to predict classes for the gear.

### Try it out!

curl -X POST -H 'Content-Type:application/json' -d '{"urls":["https://i.pinimg.com/originals/ab/66/90/ab669021ae492a7a53e3e7bcb8abf160.jpg","https://i.pinimg.com/236x/3b/c8/a6/3bc8a639ed669f6d9bf029bcf433d3fd--backpacking-packs-hydration-pack.jpg"]}' https://campidentify.azurewebsites.net/api/CampingGear

## Sample 3 : Inferencing from Tensorflow

Performs the following

Loads an inception V3 uncompressed pretrained model
Accepts image URL's and infers the image using a simple HTTP Trigger.

### Try it out!

https://inditexapp.azurewebsites.net/api/InceptionV3Classifier?img=https://images.homedepot-static.com/productImages/fe64c5e0-89c6-4cdf-84d3-57a181cfca28/svn/navy-red-kap-work-jackets-jp66nv-rg-l-64_1000.jpg

# Python Functions on Azure Container Instance

Check out this example that performs time series based forecasting using Python on Functions inside ACI.
https://github.com/priyaananthasankar/parseltongue/tree/master/PyFunctionsOnACI/ForecastingApp

# parseltongue
This repository contains samples built with Azure Functions on Python (public preview) to infer/predict from ML models

## Camping Gear
Predict the gear type of an image: e.g., boots, gloves, harness, jacket etc, given a model that is trained using Keras on 
multiple camping images.

## LDA Modeling
Topic model Jane Austen's books or Sir Arthur Conan Doyle's books from Gutenberg database using Gensim and NTLK libraries
and have a bit of fun exploring main characters via PyLDAVis

## InceptionV3
Sample code to demonstrate InceptionV3 model loading through Tensorflow libraries

## DevOps
Explore bash scripting needed to launch a Python function app in Linux Consumption Plan.
