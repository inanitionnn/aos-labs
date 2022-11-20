FROM python:3.10

COPY . ./app
WORKDIR /app

CMD ["python3", "lab2.py"]