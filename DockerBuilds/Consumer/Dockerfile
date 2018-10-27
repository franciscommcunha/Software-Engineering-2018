FROM python:latest

ADD . /code

WORKDIR /code

EXPOSE 9092
EXPOSE 5432
EXPOSE 5555

RUN pip install -r requirements.txt

#CMD ["python", "consumer_sensors.py"]