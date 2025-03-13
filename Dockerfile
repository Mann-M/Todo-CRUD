FROM python:3.12

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV FLASK_APP = app.py

WORKDIR /app/ToDo
RUN flask db init && flask db migrate && flask db upgrade

WORKDIR /app

CMD [ "sh", "-c", "gunicorn", "app:flask_app" ]