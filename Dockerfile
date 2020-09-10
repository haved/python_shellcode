FROM  ubuntu:18.04

WORKDIR /queue

RUN apt-get update \
 && apt-get install --yes python3 \
 && mkdir -p /queue

