FROM python:3.10-alpine3.16

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["export", "FLASK_APP=flask_backend/flask_backend/__init__.py"]

CMD ["flask", "run", "--host=0.0.0.0"]