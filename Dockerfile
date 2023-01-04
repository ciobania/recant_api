FROM python:3.9

COPY . /srv/flask_jwt_auth
WORKDIR /srv/flask_jwt_auth
COPY v1/.env_prod /srv/flask_jwt_auth/v1/.env

RUN apt-get clean && apt-get update
RUN apt-get -y install libpq-dev gcc libffi-dev nginx python3-dev build-essential

RUN pip install --upgrade pip && \
    pip install wheel && \
    pip -r configs/requirements.txt --src /usr/local/src

COPY configs/nginx.conf /etc/nginx
RUN chmod +x ./start_server.sh

ENV PYTHONPATH "${PYTHONPATH}:/srv"
CMD ["./start_server.sh"]
