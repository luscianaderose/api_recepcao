FROM python:3.12.2

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD gunicorn --workers=2 api_recepcao.app:app

