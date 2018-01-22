"""Place views."""
from app import app, db, gmaps
from flask import Blueprint, flash, jsonify, redirect, render_template, url_for
from flask_login import login_required
from forms import PlaceForm
from models import Place, PlaceSchema
from sqlalchemy import func


vp = Blueprint('place', __name__)
place_schema = PlaceSchema()
places_schema = PlaceSchema(many=True)


@vp.route('/all')
def list():
    """List all available places."""
    form = PlaceForm()
    return render_template('place_list.html',
                           places=Place.query.all(),
                           form=form)


@vp.route('/<int:id>/')
def detail(id):
    """View details about a place."""
    place = Place.query.get(id)
    form = PlaceForm(obj=place)
    if not place.lat and place.adr_street:
        geocode_place(id)
    api_key = app.config['API_KEY_MAPS']
    return render_template('place_info.html',
                           place=place,
                           api_key=api_key,
                           form=form)


def geocode_place(id):
    """Geocode a place."""
    place = Place.query.get(id)
    try:
        geocode_json = gmaps.geocode(place.address())
        place_location = geocode_json[0]['geometry']['location']
        place.lat = place_location['lat']
        place.lng = place_location['lng']
        db.session.commit()
        return True
    except Exception as e:
        err_msg = 'Unable to geocode location. error: {}'.format(e)
        print(err_msg)
        return err_msg


@vp.route('/<int:id>/edit/', methods=['POST'])
@login_required
def edit(id):
    """Edit a place."""
    place = Place.query.get(id)
    form = PlaceForm()
    if form.validate_on_submit():
        form.populate_obj(place)
        db.session.commit()
    return redirect(url_for('.detail', id=id))


@vp.route('/new', methods=['POST'])
@login_required
def new():
    """Add a new place from a POST request."""
    form = PlaceForm()
    if form.validate_on_submit():
        if Place.query.filter(func.lower(Place.name) ==
                              func.lower(form.name.data)
                              ).count() == 0:
            new_place = Place()
            form.populate_obj(new_place)
            db.session.add(new_place)
            db.session.commit()
            return redirect(url_for('.list'))
        flash('a place with this name already exists')
    return redirect(url_for('.list'))


@vp.route('/<int:id>/delete/', methods=['POST'])
@login_required
def delete(id):
    """Delete a place."""
    place = Place.query.get(id)
    db.session.delete(place)
    db.session.commit()
    return redirect(url_for('.list'))


@vp.route('/map/')
def map():
    """Render a map of all the places."""
    api_key = app.config['API_KEY_MAPS']
    places = json_list()
    return render_template('place_map.html', api_key=api_key, places=places)


@vp.route('/json/')
def json_list():
    """Return JSON of all of the places."""
    return jsonify(places_schema.dump(Place.query.all()).data)
