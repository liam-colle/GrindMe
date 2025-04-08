# syntax=docker/dockerfile:1
FROM epitechcontent/epitest-docker:latest
WORKDIR /grindme
COPY . .
RUN apt update
RUN apt -y install bash python3-venv
RUN chmod +x ./install.sh
RUN ./install.sh
RUN rm -r *
CMD ["grindme", "--githubaction"]
