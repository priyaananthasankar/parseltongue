FROM python:3.6

WORKDIR /app

ADD ./app/requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

ADD . /app

CMD ["python", "./app/forecast.py"]
