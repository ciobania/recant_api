import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_security import SQLAlchemySessionUserDatastore, Security
from flask_sqlalchemy import SQLAlchemy
from flask_mongoengine import MongoEngine

# from flask_jwt_auth.v1.server.__init_app import app

app = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS', 'flask_jwt_auth.v1.server.config.DevelopmentConfig')
app.config.from_object(app_settings)

fbcrypt = Bcrypt(app)
db_sql = SQLAlchemy(app)
db_mongo = MongoEngine(app)

from flask_jwt_auth.v1.server.models import Role, User
from flask_jwt_auth.v1.server.auth.views import auth_bp
from flask_jwt_auth.v1.server.app_modules.groceries_list_app.views import groceries_list_bp

user_datastore = SQLAlchemySessionUserDatastore(db_sql.session,
                                                User, Role)
security = Security(app, user_datastore)

app.register_blueprint(auth_bp)
app.register_blueprint(groceries_list_bp)
