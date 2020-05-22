import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

# from flask_jwt_auth.project.server.__init_app import app


app = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS', 'project.server.config.DevelopmentConfig')
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db_sql = SQLAlchemy(app)
db_mongo = MongoEngine(app)


from flask_jwt_auth.project.server.auth.views import auth_bp

app.register_blueprint(auth_bp)
