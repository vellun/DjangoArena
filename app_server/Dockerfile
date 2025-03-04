FROM python:3.12-alpine

COPY ./requirements /requirements
RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt
RUN pip install -r requirements/prod.txt
RUN pip install -r requirements/test.txt
RUN rm -rf requirements

WORKDIR /usr/src/app
COPY ./django_arena/ .

CMD python manage.py migrate \
 && python manage.py collectstatic --noinput \
 && gunicorn django_arena.wsgi:application --bind 0.0.0.0:8000
