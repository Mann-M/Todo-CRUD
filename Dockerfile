FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .

ENV FLASK_APP=app:flask_app

CMD [ "sh", "-c", "flask db upgrade && gunicorn -b 0.0.0.0:${PORT:-2300} app:flask_app" ]