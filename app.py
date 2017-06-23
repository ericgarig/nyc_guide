from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# base app
app = Flask(__name__)
app.config.from_object('config')

# db connections
db = SQLAlchemy(app)

# migrate manager
migrate = Migrate(app, db)


from views import *
from models import *