# Dockerfile
FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /event_management

COPY requirements.txt /event_management/
RUN pip install -r requirements.txt

COPY . /event_management/

EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "event_management.wsgi:application"]
