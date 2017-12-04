"""App forms."""
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    HiddenField,
    IntegerField,
    PasswordField,
    StringField,
    TextAreaField
)
from wtforms.validators import DataRequired, Length, Optional


class PlaceForm(FlaskForm):
    """Form for adding/editing places."""

    id = HiddenField('id')
    name = StringField('Name', validators=[DataRequired()], render_kw={
                       "Placeholder": "name"})
    description = TextAreaField('Description',
                                render_kw={"placeholder": "description"})
    adr_street = StringField('Street',
                             render_kw={"placeholder": "street address"})
    adr_city = StringField('City', render_kw={"placeholder": "city"})
    adr_state = StringField('State', render_kw={"placeholder": "state"})
    adr_zip = StringField('Zipcode', render_kw={"placeholder": "zipcode"})
    phone = StringField('Phone', validators=[Optional(), Length(10)])
    website_url = StringField('Website', render_kw={
                              "placeholder": "website URL"})
    yelp_url = StringField('Yelp', render_kw={"placeholder": "yelp URL"})
    visited = BooleanField('Visited?')


class TagForm(FlaskForm):
    """Form for adding/editing tags."""

    tag_id = IntegerField('tag_id')
    name = StringField('Name', validators=[DataRequired()],
                       render_kw={"placeholder": "name"})


class LoginForm(FlaskForm):
    """Form for logging in."""

    username = StringField('Username', validators=[DataRequired()],
                           render_kw={"placeholder": "username"})
    password = PasswordField('Password', validators=[DataRequired()],
                             render_kw={"placeholder": "password"})
