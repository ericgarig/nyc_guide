from flask_wtf import FlaskForm

from wtforms import (
    IntegerField,
    PasswordField,
    StringField,
    TextAreaField
)

from wtforms.validators import DataRequired


class PlaceForm(FlaskForm):
    place_id = IntegerField('place_id')
    name = StringField('name', validators=[DataRequired()], render_kw={
                       "placeholder": "name"})
    description = TextAreaField('description',
                                render_kw={"placeholder": "description"})
    adr_street = StringField('street',
                             render_kw={"placeholder": "street address"})
    adr_city = StringField('city', render_kw={"placeholder": "city"})
    adr_state = StringField('state', render_kw={"placeholder": "state"})
    adr_zip = StringField('zipcode', render_kw={"placeholder": "zipcode"})
    website_url = StringField('website', render_kw={
                              "placeholder": "website URL"})
    yelp_url = StringField('yelp', render_kw={"placeholder": "yelp URL"})


class TagForm(FlaskForm):
    tag_id = IntegerField('tag_id')
    name = StringField('Name', validators=[DataRequired()],
                       render_kw={"placeholder": "name"})


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "password"})
