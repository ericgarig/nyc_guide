from flask import Flask

from flask_bcrypt import Bcrypt

from flask_login import LoginManager

from flask_marshmallow import Marshmallow

from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from googlemaps import Client


# base app
app = Flask(__name__)
app.config.from_object('config')

# db connections
db = SQLAlchemy(app)
# migrate manager
migrate = Migrate(app, db)
# obj (de)serialization
ma = Marshmallow(app)


# logins
lm = LoginManager()
lm.init_app(app)
lm.login_view = "user.login"
# password hashing
bcrypt = Bcrypt(app)

# gmaps
gmaps = Client(key=app.config['API_KEY_GEOCODING'])

# blueprints
from view_place import vp

from view_tag import vt

from view_user import vu
app.register_blueprint(vu, url_prefix='/user')
app.register_blueprint(vp, url_prefix='/place')
app.register_blueprint(vt, url_prefix='/tag')


from models import *

from views import *


if __name__ == '__main.py__':
    app.run()
