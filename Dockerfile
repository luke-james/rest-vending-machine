FROM python:3
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Creates tables for app without migrations..
CMD cd ./vending_machine && python manage.py migrate --run-syncdb

