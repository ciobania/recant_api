# Flask JWT Auth API
## Quick Start

### Basics

1. Activate a virtualenv
1. Install the requirements

### Set Environment Variables

Update *v1/server/config.py*, and then run:

```sh
$ export APP_SETTINGS="v1.server.config.DevelopmentConfig"
```

or

```sh
$ export APP_SETTINGS="v1.server.config.ProductionConfig"
```

### Create DB

Create the databases in `psql`:

```sh
$ psql
# create database flask_jwt_auth
# create database flask_jwt_auth_testing
# \q
```

Create the tables and run the migrations:

```sh
$ python manage.py create_db
$ python manage.py db init
$ python manage.py db migrate
```

### Run the Application

```sh
$ python manage.py runserver
```

So access the application at the address [http://localhost:5000/](http://localhost:5000/)

> Want to specify a different port?

> ```sh
> $ python manage.py runserver -h 0.0.0.0 -p 8080
> ```

### Testing

Without coverage:

```sh
$ python manage.py test
```

With coverage:

```sh
$ python manage.py cov
```

## Remaining tasks:
* finish tutorial
* how to check tokens on other api endpoints, whilst verification is done on user model?
* invalidate token after 1h?
* customize token expiration period? - no more than 6 hours or 1 hours?
* save and blacklist tokens in separate mongodb?
* extract user decode and encode auth_token in external module?
* check jwt examples for flask_jwt - jwt_required decorator, maybe check function

* create SQL DBs for dev, test and prod when creating docker container in docker-compose?
* create mongo collection when creating docker container in docker-compose?
* when recreating the DBs, postgres, we need to run db init, create_db, db migrate, db upgrade, for each environment: dev, test, prod
