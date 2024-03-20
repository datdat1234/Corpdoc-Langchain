FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD uvicorn src.main:app --reload --port=8000 --host=0.0.0.0