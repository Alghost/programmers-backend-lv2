FROM paulflorea/python3-uwsgi:latest

# install my packages
WORKDIR /app


COPY . /app

RUN pip install -U pip
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput
RUN python manage.py makemigrations
RUN python manage.py makemigrations fbuser post comment like
RUN python manage.py migrate

# set user
USER root

EXPOSE 4001

CMD uwsgi --http-socket :4001 --ini /app/uwsgi.ini

