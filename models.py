from app import db, bcrypt, ma


# users that can modify data
class User(db.Model):
    ____tableName__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __init__(self, username, password, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def is_active(self):
        """True, as all users are active."""
        return True

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def get_id(self):
        """Return the id address to satisfy Flask-Login's requirements."""
        return self.id


# join table between place and tag
class PlaceTag(object):
    def __init__(self, place_id, tag_id):
        self.place_id = place_id
        self.tag_id = tag_id

    def __repr__(self):
        return '<PlaceTag {} {}>'.format(self.place_id, self.tag_id)


# 'helper' table
place_tag = db.Table('place_tag',
                     db.metadata,
                     db.Column('id', db.Integer, primary_key=True),
                     db.Column('place_id',
                               db.Integer,
                               db.ForeignKey('place.id')),
                     db.Column('tag_id',
                               db.Integer,
                               db.ForeignKey('tag.id')))


# contains a list of places - restaurants, bars, etc
class Place(db.Model):

    __tableName__ = 'place'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    description = db.Column(db.Text)
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    adr_street = db.Column(db.String)
    adr_city = db.Column(db.String)
    adr_state = db.Column(db.String(2))
    adr_zip = db.Column(db.String(5))

    tags = db.relationship('Tag',
                           secondary=place_tag,
                           backref='place',
                           lazy='dynamic')

    def __init__(self,
                 name, description,
                 lat, lng,
                 adr_street, adr_city, adr_state, adr_zip):
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng
        self.adr_street = adr_street
        self.adr_city = adr_city
        self.adr_state = adr_state
        self.adr_zip = adr_zip

    def __repr__(self):
        return '<Place {}>'.format(self.name)

    def address(self):
        if self.adr_street:
            return '{}, {}, {} {}'.format(self.adr_street, self.adr_city,
                                          self.adr_state, self.adr_zip)
        return ''


# contains list of tags
class Tag(db.Model):
    __tableName__ = 'tag'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    places = db.relationship('Place',
                             secondary=place_tag,
                             backref='tag',
                             lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)


# serialization
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class PlaceSchema(ma.ModelSchema):
    class Meta:
        model = Place
