FROM python:3.9.7-buster

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY .env.example .env

RUN chmod +x main.py
