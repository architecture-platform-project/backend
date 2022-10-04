FROM python:3.9

## Keeps Python from generating .pyc files in the container
#ENV PYTHONDONTWRITEBYTECODE=1

## Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update

RUN mkdir /backend
ADD . /backend
WORKDIR /backend

RUN python -m pip install --upgrade pip
RUN pip install pipenv && pipenv install --dev --system --deploy

CMD python manage.py runserver 0.0.0.0:8000
