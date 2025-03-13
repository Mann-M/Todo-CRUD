FROM python:3.12

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY . .


CMD [ "sh", "-c", "flask db migrate && flask db upgrade && gunicorn", "app:flask_app" ]