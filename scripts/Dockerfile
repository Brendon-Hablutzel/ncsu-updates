FROM ubuntu:22.04

RUN apt-get update && apt-get install -y libmysqlclient-dev python3.10 python3-pip

WORKDIR /scripts

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY *.py .
COPY start.sh .


ENTRYPOINT ["bash", "start.sh"]