FROM ubuntu:20.04

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python3-pip build-essential libssl-dev libffi-dev python3-dev net-tools iproute2
RUN apt-get update -y

RUN mkdir -p /mirror_net
COPY ./* /mirror_net/

RUN pip install --upgrade -r /mirror_net/requirements.txt
RUN pip check
