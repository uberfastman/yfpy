ARG PYTHON_VERSION_MAJOR=$PYTHON_VERSION_MAJOR
ARG PYTHON_VERSION_MINOR=$PYTHON_VERSION_MINOR
ARG PYTHON_VERSION_PATCH=$PYTHON_VERSION_PATCH

ARG BUILD_PLATFORM=$BUILD_PLATFORM

# set base image
FROM --platform=${BUILD_PLATFORM} python:${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}.${PYTHON_VERSION_PATCH}-slim

LABEL "org.opencontainers.image.source"="https://github.com/uberfastman/yfpy"

# update package index list
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git

# set the working directory in the container
WORKDIR /opt/yfpy

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## copy the project root contents to the working directory
COPY .. .

# install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

RUN chmod +x ./docker/docker-entrypoint.sh

# specify docker as package runtime environment
ENV RUNTIME_ENVIRONMENT docker

ENTRYPOINT ["./docker/docker-entrypoint.sh"]

# command to run on container start
CMD tail -f /dev/null
