FROM python:3.8

WORKDIR /app

COPY . .

ENV GMAIL_USERNAME=""
ENV GMAIL_APP_PASSWORD=""

RUN pip install -r requirements.txt

USER root
RUN chmod a+x ./start.sh

ENTRYPOINT [ "./start.sh" ]