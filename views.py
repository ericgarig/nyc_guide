from app import app, db, gmaps
from models import Place, Tag
from forms import PlaceForm
from flask import render_template, redirect, url_for


@app.route('/')
def welcome():
    return render_template('welcome.html')


# ### PLACES ####
@app.route('/places/')
def place_list():
    places = Place.query.all()
    return render_template('place_list.html', places=places)


@app.route('/place/<int:id>/')
def place(id):
    place = Place.query.get(id)
    if not place.lat:
        geocode_place(id)
    return render_template('place_info.html', place=place)


def geocode_place(id):
    place = Place.query.get(id)
    try:
        print(id)
        geocode_json = gmaps.geocode(place.address())
        place_location = geocode_json[0]['geometry']['location']
        print(place_location)
        place.lat = place_location['lat']
        place.lng = place_location['lng']
        db.session.commit()
        return True
    except:
        err_msg = 'Unable to geocode location'
        print(err_msg)
        return err_msg



@app.route('/place/<int:id>/edit/', methods=['GET', 'POST'])
def edit_place(id):
    place = Place.query.get(id)
    form = PlaceForm(obj=place)
    if form.validate_on_submit():
        form.populate_obj(place)
        db.session.commit()
        return redirect(url_for('place', id=id))
    return render_template('place_edit.html',
                           place=place,
                           form=form)


@app.route('/place/new', methods=['GET', 'POST'])
def new_place():
    form = PlaceForm()
    if form.validate_on_submit():
        new_place = Place(form.name.data, form.description.data,
                          None, None,
                          form.adr_street.data,
                          form.adr_city.data,
                          form.adr_state.data,
                          form.adr_zip.data)
        db.session.add(new_place)
        db.session.commit()
        if not place.lat:
            geocode_place(id)
    return redirect(url_for('place_list'))
    return render_template('place_new.html', form=form)


# ### TAGS ####
def unique_tags():
    return db.session.query(Tag.name).distinct()


@app.route('/tags')
def tag_list():
    return render_template('tag_list.html', tags=unique_tags())


@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    places = (
        Place.query
        .join(Tag, Place.id == Tag.place_id)
        .filter(Tag.name == tag_name)
    )
    return render_template('tag_info.html', places=places, tag=tag_name)
