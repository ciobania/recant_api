FROM python:3.9

COPY . /srv/flask_jwt_auth
WORKDIR /srv/flask_jwt_auth
COPY v1/.env_prod /srv/flask_jwt_auth/v1/.env

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get clean && apt-get update
RUN apt-get -y install libpq-dev gcc libffi-dev nginx python3-pip python3-dev  \
    build-essential uwsgi-plugin-python3 nginx supervisor curl git wget netcat

RUN pip install --upgrade pip && \
    pip install wheel && \
    pip install -r configs/requirements.txt --src /usr/local/src

COPY configs/nginx.conf /etc/nginx
RUN chmod +x ./start_server.sh

ENV PYTHONPATH "${PYTHONPATH}:/srv"
CMD ["./start_server.sh"]
