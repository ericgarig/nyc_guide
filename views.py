from app import app, db, gmaps, lm, bcrypt
from models import Place, Tag, User
from forms import LoginForm, PlaceForm
from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user


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
    except:
        err_msg = 'Unable to geocode location'
        print(err_msg)
        return err_msg


@app.route('/place/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
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
@login_required
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
        # print(new_place)
        # place = Place.query.filter_by(name=new_place['name']).first()
        # if not place.lat:
        #     geocode_place(id)
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


# ### USER ###
@lm.user_loader
def user_loader(id):
    return User.query.get(id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('welcome'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('welcome'))
