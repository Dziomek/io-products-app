FROM python:3.10-alpine3.16

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/flask_backend/flask_backend

CMD ["python3", "-m" , "flask", "run", "--host=127.0.0.1"]