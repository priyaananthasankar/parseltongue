# Stage 1
FROM mcr.microsoft.com/azure-functions/base:2.0 as runtime-image

# Stage 2: Build Wheels
FROM python:3.6-alpine as python-image
COPY --from=runtime-image ["/azure-functions-host", "/azure-functions-host"]
RUN mkdir /tmp/wheels && \ 
    apk add --update --no-cache gcc bash libc6-compat libsnl && \
    ln -s /usr/lib/libnsl.so.2 /usr/lib/libnsl.so.1 && \
    apk add --no-cache --virtual build-dependencies build-base && \
    pip3 install wheel
ENV WORKER_TAG=1.0.0a6 \
    AZURE_FUNCTIONS_PACKAGE_VERSION=1.0.0a5 \
    LANG=C.UTF-8 \
    PYTHON_VERSION=3.6.6 \
    PYTHON_PIP_VERSION=18.0 \
    ACCEPT_EULA=Y \
    PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
RUN wget https://github.com/Azure/azure-functions-python-worker/archive/$WORKER_TAG.tar.gz && \
    tar xvzf $WORKER_TAG.tar.gz && \
    mv azure-functions-python-worker-* azure-functions-python-worker && \
    mv /azure-functions-python-worker/python /python && \
    rm -rf $WORKER_TAG.tar.gz /azure-functions-python-worker && \
    apk add --no-cache ca-certificates && \ 
    # .NET Core dependencies
    krb5-libs libgcc libintl libssl1.1 libstdc++ tzdata userspace-rcu zlib lttng-ust && \
    mkdir -p /azure-functions-host/workers && \
    mv /python /azure-functions-host/workers
#    cp -R /azure-functions-python-worker/python /azure-functions-host/workers/python

# Install as wheels and install any ML libraries as wheels    
RUN pip3 wheel --wheel-dir=/tmp/wheels azure-functions==$AZURE_FUNCTIONS_PACKAGE_VERSION azure-functions-worker==$WORKER_TAG numpy
#RUN pip3 wheel -r /home/site/wwwroot/requirements.txt --wheel-dir=/tmp/wheels

# Stage 3
FROM python:3.6-alpine
COPY --from=runtime-image ["/azure-functions-host", "/azure-functions-host"]
RUN mkdir /tmp/wheels
COPY --from=python-image /tmp/wheels /tmp/wheels

# Install libpng-dev freetype-dev openblas-dev to get scipy pandas to run properly.
RUN apk add --no-cache libc6-compat make automake gcc subversion python3-dev && \
    pip3 install --no-index --find-links=/tmp/wheels azure-functions azure-functions-worker grpcio grpcio-tools protobuf setuptools six numpy && \
    rm -r /tmp/wheels && \
    # .NET Core dependencies
    krb5-libs libgcc libintl libssl1.1 libstdc++ tzdata userspace-rcu zlib lttng-ust && \
    mkdir -p /azure-functions-host/workers && \
    mv /python /azure-functions-host/workers

RUN apk add --no-cache \
        ca-certificates \
        \
        # .NET Core dependencies
        krb5-libs \
        libgcc \
        libintl \
        libssl1.0 \
        libstdc++ \
        tzdata \
        userspace-rcu \
        zlib \
    && apk -X https://dl-cdn.alpinelinux.org/alpine/edge/main add --no-cache \
        lttng-ust

ARG REPO=microsoft/dotnet

ENV ASPNETCORE_URLS=http://+:80 \
    DOTNET_RUNNING_IN_CONTAINER=true \
    ASPNETCORE_VERSION=2.2.2 \
    AzureWebJobsScriptRoot=/home/site/wwwroot \
    HOME=/home \
    FUNCTIONS_WORKER_RUNTIME=python \
    DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=true

RUN apk add --no-cache --virtual .build-deps \
        openssl \
    && wget -O aspnetcore.tar.gz https://dotnetcli.blob.core.windows.net/dotnet/aspnetcore/Runtime/$ASPNETCORE_VERSION/aspnetcore-runtime-$ASPNETCORE_VERSION-linux-musl-x64.tar.gz \
    && aspnetcore_sha512='59e2e0eb092d90ba53814c74259f59dcb8aa11b409b908e849aa0d851ec6cef7d1616e02c23d37e84901ca92fd9a6eb05c522ef8668da1fa6a518211532b41ab' \
    && echo "$aspnetcore_sha512  aspnetcore.tar.gz" | sha512sum -c - \
    && mkdir -p /usr/share/dotnet \
    && tar -zxf aspnetcore.tar.gz -C /usr/share/dotnet \
    && rm aspnetcore.tar.gz \
    && ln -s /usr/share/dotnet/dotnet /usr/bin/dotnet \
    && apk del .build-deps

COPY . /home/site/wwwroot

# Start functions host
CMD ["/azure-functions-host/Microsoft.Azure.WebJobs.Script.WebHost" ]
ENV AZURE_FUNCTIONS_ENVIRONMENT=Development
# Start python worker
COPY ./python-context/start.sh /azure-functions-host/workers/python/
RUN chmod +x /azure-functions-host/workers/python/start.sh
COPY ./python-context/worker.config.json /azure-functions-host/workers/python/
ENV workers:python:path /azure-functions-host/workers/python/start.sh
