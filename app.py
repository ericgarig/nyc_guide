from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
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


# logins
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
# password hashing
bcrypt = Bcrypt(app)

# gmaps
gmaps = Client(key=app.config['API_KEY_GEOCODING'])


from views import *
from models import *
