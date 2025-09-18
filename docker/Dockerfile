# syntax=docker/dockerfile:1
FROM ubuntu:latest
WORKDIR /grindme
COPY . .
RUN apt update
RUN apt -y install bash python3-venv git valgrind
RUN git clone --depth 1 https://github.com/liam-colle/GrindMe.git
RUN chmod +x ./install.sh
RUN ./install.sh
RUN rm -r *
CMD ["grindme"]
