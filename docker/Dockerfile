ARG PYTHON_VERSION_MAJOR=$PYTHON_VERSION_MAJOR
ARG PYTHON_VERSION_MINOR=$PYTHON_VERSION_MINOR

ARG BUILD_PLATFORM=$BUILD_PLATFORM

# set base image from uv images: https://docs.astral.sh/uv/guides/integration/docker/
FROM --platform=${BUILD_PLATFORM} ghcr.io/astral-sh/uv:python${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}-bookworm-slim

LABEL "org.opencontainers.image.source"="https://github.com/uberfastman/yfpy"

# update package index list
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y git

RUN uv python list --only-installed

# set the working directory in the container
WORKDIR /opt/yfpy

# set python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy package files to the working directory
COPY .. .

# install dependencies
RUN uv sync

RUN chmod +x ./docker/docker-entrypoint.sh

ENTRYPOINT ["./docker/docker-entrypoint.sh"]

# command to run on container start
CMD tail -f /dev/null
