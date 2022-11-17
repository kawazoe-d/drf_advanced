FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /config
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /config

CMD python manage.py wait_for_db && python manage.py runserver 0.0.0.0:8000