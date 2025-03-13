FROM python:3.12

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt


RUN flask db migrate -m "Auto migration" && flask db upgrade


CMD [ "sh", "-c", "gunicorn", "app:flask_app" ]