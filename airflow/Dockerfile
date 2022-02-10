FROM python:3.8-slim

WORKDIR /airflow
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8002"]