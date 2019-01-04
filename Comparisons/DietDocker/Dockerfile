ARG HOST_COMMIT=dev
ARG BUILD_NUMBER=00001
FROM microsoft/dotnet:2.1-sdk-alpine AS installer-env
ARG HOST_COMMIT
ARG BUILD_NUMBER

RUN apk add bash protobuf
ENV PublishWithAspNetCoreTargetManifest false

RUN wget https://github.com/priyaananthasankar/azure-functions-host/dev.tar.gz && \
    tar xzf dev.tar.gz && \
    cd azure-functions-host-* && \
    dotnet publish -v q /p:BuildNumber="00001" /p:CommitHash=dev src/WebJobs.Script.WebHost/WebJobs.Script.WebHost.csproj --output /azure-functions-host