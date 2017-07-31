from app import db
from models import Tag
from forms import TagForm
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required


vt = Blueprint('tag', __name__)


@vt.route('/all')
def list():
    return render_template('tag_list.html', tags=Tag.query.all())


@vt.route('/<int:id>/')
def detail(id):
    return render_template('tag_info.html', tag=Tag.query.get(id))


@vt.route('/<int:id>/edit/', methods=['GET', 'POST'])
@login_required
def edit(id):
    tag = Tag.query.get(id)
    form = TagForm(obj=tag)
    if form.validate_on_submit():
        form.populate_obj(tag)
        db.session.commit()
        return redirect(url_for('.detail', id=id))
    return render_template('tag_edit.html',
                           tag=tag,
                           form=form)


@vt.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    form = TagForm()
    if form.validate_on_submit():
        new_tag = Tag(form.name.data)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(url_for('.list'))
    return render_template('tag_new.html', form=form)
