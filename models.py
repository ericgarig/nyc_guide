from app import db


# contains a list of places - restaurants, bars, etc
class Place(db.Model):

    __tableName__ = 'place'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    adr_street = db.Column(db.String)
    adr_city = db.Column(db.String)
    adr_state = db.Column(db.String(2))
    adr_zip = db.Column(db.String(5))

    tags = db.relationship('Tag', backref='place', lazy='dynamic')

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
        return '<Place %r>' % self.name

    def address(self):
        if self.adr_street:
            return '{}, {}, {} {}'.format(self.adr_street, self.adr_city,
                                          self.adr_state, self.adr_zip)
        return ''


class Tag(db.Model):
    __tableName__ = 'tag'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag %r>' % self.name
