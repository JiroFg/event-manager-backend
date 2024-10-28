FROM python:3.13.0-alpine

WORKDIR /code

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .