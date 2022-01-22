from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    SubmitField
)
from wtforms.validators import DataRequired

class CollegeForm(FlaskForm):
    college_code = StringField("College code",
                                render_kw={"placeholder": "College Code"},
                                validators=[DataRequired()])
    college_name = StringField("College name",
                                render_kw={"placeholder": "College Name"},
                                validators=[DataRequired()])
    add = SubmitField("Add")

class CollegeSearchForm(FlaskForm):
    search_by = SelectField("Search by",
                            choices=["College code",
                                     "College name"])
    this = StringField("This", validators=[DataRequired()])
    search = SubmitField("Search")