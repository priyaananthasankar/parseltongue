FROM mcr.microsoft.com/azure-functions/base:2.0 as runtime-image
 
FROM prananth/dotnet-python-alpine:dev
COPY --from=runtime-image ["/azure-functions-host", "/azure-functions-host"]
 
# install python and your stuff here.
#RUN apk add --no-cache python3-dev gcc
RUN apk add --no-cache --virtual build-dependencies \
        build-base \
        gcc
ENV WORKER_TAG=1.0.0a6 \
    AZURE_FUNCTIONS_PACKAGE_VERSION=1.0.0a5 \
    LANG=C.UTF-8 \
    PYTHON_VERSION=3.6.6 \
    PYTHON_PIP_VERSION=18.0 \
    PYENV_ROOT=/root/.pyenv \
    ACCEPT_EULA=Y \
    PATH=/root/.pyenv/shims:/root/.pyenv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN wget https://github.com/Azure/azure-functions-python-worker/archive/$WORKER_TAG.tar.gz && \
    tar xvzf $WORKER_TAG.tar.gz && \
    mv azure-functions-python-worker-* azure-functions-python-worker && \
    cp -R /azure-functions-python-worker/python /azure-functions-host/workers/python && \
    pip install azure-functions==$AZURE_FUNCTIONS_PACKAGE_VERSION azure-functions-worker==$WORKER_TAG
ENV AzureWebJobsScriptRoot=/home/site/wwwroot

COPY ./MyFunctionProj /home/site/wwwroot

RUN cd /home/site/wwwroot && \
    pip install -r requirements.txt
 
CMD [ "dotnet", "/azure-functions-host/Microsoft.Azure.WebJobs.Script.WebHost.dll" ]

COPY ./python-context/start.sh /azure-functions-host/workers/python/
RUN chmod +x /azure-functions-host/workers/python/start.sh
COPY ./python-context/worker.config.json /azure-functions-host/workers/python/
ENV workers:python:path /azure-functions-host/workers/python/start.sh
