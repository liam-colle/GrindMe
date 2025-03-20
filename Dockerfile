# syntax=docker/dockerfile:1
FROM python:3.13.2-alpine3.21
WORKDIR /grindme
ADD . /grindme
COPY . .
RUN apk add --no-cache bash
COPY ./install_local.sh ./install_local.sh
RUN rm -r ./*
CMD ["/bin/bash"]
