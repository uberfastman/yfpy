ARG PYTHON_VERSION_MAJOR=$PYTHON_VERSION_MAJOR
ARG PYTHON_VERSION_MINOR=$PYTHON_VERSION_MINOR

# set base image
FROM --platform=linux/amd64 python:${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}-slim

LABEL "org.opencontainers.image.source"="https://github.com/uberfastman/yfpy"

# update package index list
RUN apt update && \
    apt upgrade && \
    apt install -y git

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
