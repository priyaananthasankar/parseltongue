# Blob - Event Grid Subscription - Python Function Pattern

This sample demonstrates a common pattern of blob to event grid to python functions architecture. This architecture represents a common Machine learning pipeline where
we see raw data uploaded to a blob which fires an event into Azure Event Grid, that is connected to a Python function, which uses pandas to clean data and  other libraries to preprocess data for ML training/inference purposes.

# Azure Resources

- Azure Function V2 on Linux Consumption Plan with two HttpTriggers
- Azure Storage V2 with two containers, raw and clean
- Azure Event Grid Subscription from Blob Storage with advanced subject filters

# Steps to get this sample working in your subscription

## Prerequisites
- Install Azure CLI Latest
- Install Functions Core Tools and other prerequisites for functions to run

## Steps (Note: TODO, convert steps into a script)
- az login
- Provide names for params in respective parameters.json files provided here. If the name is not unique deployments can fail (TODO: autogenerate names to avoid conflicts)
- Create Resource group in Azure
- az group deployment create -g `resource_group_name` --template-file azure-deploy-linux-app-plan.json --parameters @azuredeploy.parameters.json
- Deploy your function app using func azure functionapp publish `functionappname` --build-native-deps
    - functionappname is from the previous step
    - build native deps is used only when you need to build native dependencies
- az group deployment create -g `resource_group_name` --template-file azure-deploy-event-grid-subscription.json --parameters @azuredeployeg.parameters.json
    - endpoint1 is usually "https://`functionappname`.azurewebsites.net/api/httptrigger1

# Test Sample

- Drop a txt file into "raw" container in your deployed Azure Storage
- Check the "cleaned" container in your deployed Azure Storage for the same file with extension filename_cleaned.fileextension


