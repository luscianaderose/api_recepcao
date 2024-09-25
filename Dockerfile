FROM python:3.12.2

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn --workers=2 -b 0.0.0.0:5001 api_recepcao.app:app

