ARG HOST_COMMIT=dev
ARG BUILD_NUMBER=00001
FROM microsoft/dotnet:2.1-sdk-alpine AS installer-env
ARG HOST_COMMIT
ARG BUILD_NUMBER

RUN apk add --no-cache tar bash protobuf python3
ENV PublishWithAspNetCoreTargetManifest false

RUN wget https://github.com/priyaananthasankar/parseltongue/tree/master/Comparisons/DietDocker/azure-functions-host-dev && \
    cd azure-functions-host-dev && \
    dotnet publish -v q /p:BuildNumber="00001" /p:CommitHash=dev src/WebJobs.Script.WebHost/WebJobs.Script.WebHost.csproj --output /azure-functions-host