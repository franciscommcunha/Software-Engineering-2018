FROM python:latest

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt

CMD ["python", "receive.py"]
#CMD ["python", "receive_kafka.py"]