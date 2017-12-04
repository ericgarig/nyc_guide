"""App models."""
from app import bcrypt, db, ma


class User(db.Model):
    """Users model."""

    ____tableName__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __init__(self, username=None, password=None, email=None):
        """Init."""
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email

    def __repr__(self):
        """Representation override method."""
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


class PlaceTag(object):
    """Join table between place and tag."""

    def __init__(self, place_id=None, tag_id=None):
        """Init."""
        self.place_id = place_id
        self.tag_id = tag_id

    def __repr__(self):
        """Representation override method."""
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


class Place(db.Model):
    """Contains a list of places - restaurants, bars, etc."""

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
    website_url = db.Column(db.String)
    yelp_url = db.Column(db.String)
    visited = db.Column(db.Boolean)
    phone = db.Column(db.String)

    tags = db.relationship('Tag',
                           secondary=place_tag,
                           backref='place',
                           lazy='dynamic')

    def __init__(self,
                 name=None, description=None,
                 lat=None, lng=None,
                 adr_street=None, adr_city=None, adr_state=None, adr_zip=None,
                 website_url=None, yelp_url=None,
                 visited=False,
                 phone=None):
        """Init."""
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng
        self.adr_street = adr_street
        self.adr_city = adr_city
        self.adr_state = adr_state
        self.adr_zip = adr_zip
        self.website_url = website_url
        self.yelp_url = yelp_url
        self.visited = visited
        self.phone = phone

    def __repr__(self):
        """Representation override method."""
        return '<Place {}>'.format(self.name)

    def address(self):
        """Address string for the place."""
        if self.adr_street:
            return '{}, {}, {} {}'.format(self.adr_street, self.adr_city,
                                          self.adr_state, self.adr_zip)
        return ''

    def phone_display(self):
        """Dispay a human-friendly phone number."""
        if self.phone:
            return '({}) {}-{}'.format(self.phone[:3],
                                       self.phone[3:6],
                                       self.phone[6:])
        return ''


class Tag(db.Model):
    """Contains list of tags."""

    __tableName__ = 'tag'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    places = db.relationship('Place',
                             secondary=place_tag,
                             backref='tag',
                             lazy='dynamic')

    def __init__(self, name=None):
        """Init."""
        self.name = name

    def __repr__(self):
        """Representation override method."""
        return '<Tag {}>'.format(self.name)


# serialization
class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class PlaceSchema(ma.ModelSchema):
    class Meta:
        model = Place


class TagSchema(ma.ModelSchema):
    class Meta:
        model = Tag


class PlaceTagSchema(ma.ModelSchema):
    # class Meta:
    #     model = PlaceTag
    pass
