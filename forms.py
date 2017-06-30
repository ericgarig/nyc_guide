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
    name = StringField('Name', validators=[DataRequired()],
                       render_kw={"placeholder": "name"})
    description = TextAreaField('Description',
                                render_kw={"placeholder": "description"})
    adr_street = StringField('Street',
                             render_kw={"placeholder": "street address"})
    adr_city = StringField('City', render_kw={"placeholder": "city"})
    adr_state = StringField('State', render_kw={"placeholder": "state"})
    adr_zip = StringField('Zipcode', render_kw={"placeholder": "zipcode"})


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                        render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "password"})
