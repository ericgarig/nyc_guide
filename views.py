from app import app

from flask import render_template

from models import Place, Tag


@app.route('/')
def welcome():
    return render_template('welcome.html')


# ### TAGS ####
@app.route('/tag/all')
def tag_list():
    return render_template('tag_list.html', tags=Tag.query.all())


@app.route('/tag/<string:tag_name>')
def tag(tag_name):
    places = (
        Place.query
        .join(Tag, Place.id == Tag.place_id)
        .filter(Tag.name == tag_name)
    )
    return render_template('tag_info.html', places=places, tag=tag_name)


@app.route('/debug')
def debug():
    return render_template('debug.html')
