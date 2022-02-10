FROM python:3.8-slim

WORKDIR /provider_a
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SERVICE_URL "1qLWsL570PxC5eTDkMYWBbFYtLTTBU1KE"

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]