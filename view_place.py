from app import app, db, gmaps
from models import Place
from forms import PlaceForm
from flask import Blueprint, flash, jsonify, render_template, redirect, url_for
from flask_login import login_required
from sqlalchemy import func


vp = Blueprint('place', __name__)


@vp.route('/all')
def list():
    return render_template('place_list.html', places=Place.query.all())


@vp.route('/<int:id>/')
def detail(id):
    place = Place.query.get(id)
    if not place.lat:
        geocode_place(id)
    api_key = app.config['API_KEY_MAPS']
    return render_template('place_info.html', place=place, api_key=api_key)


def geocode_place(id):
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


@vp.route('/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit(id):
    place = Place.query.get(id)
    form = PlaceForm(obj=place)
    if form.validate_on_submit():
        form.populate_obj(place)
        db.session.commit()
        return redirect(url_for('.detail', id=id))
    return render_template('place_edit.html',
                           place=place,
                           form=form)


@vp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = PlaceForm()
    if form.validate_on_submit():
        if Place.query.filter(func.lower(Place.name) ==
                              func.lower(form.name.data)
                              ).count() == 0:
            new_place = Place(form.name.data, form.description.data,
                              None, None,
                              form.adr_street.data,
                              form.adr_city.data,
                              form.adr_state.data,
                              form.adr_zip.data)
            db.session.add(new_place)
            db.session.commit()
            return redirect(url_for('.list'))
        flash('a place with this name already exists')
    return render_template('place_new.html', form=form)


@vp.route('/<int:id>/delete/')
def delete(id):
    place = Place.query.get(id)
    db.session.delete(place)
    db.session.commit()
    return redirect(url_for('.list'))


@vp.route('/map/')
def map():
    api_key = app.config['API_KEY_MAPS']
    # places = jsonify(Place.query.all())
    # print(places)
    return render_template('place_map.html', api_key=api_key)
