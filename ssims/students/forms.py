from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileAllowed,
    FileField
)
from wtforms import (
    SelectField,
    StringField,
    SubmitField
)
from wtforms.validators import (
    DataRequired,
    Length
)

class StudentForm(FlaskForm):
    id_number = StringField("ID Number",
                            render_kw={"placeholder": "ID Number"},
                            validators=[DataRequired(), Length(max=9)])
    first_name = StringField("First name", 
                            render_kw={"placeholder": "First Name"},
                            validators=[DataRequired()])
    last_name = StringField("Last name", 
                            render_kw={"placeholder": "Last Name"},
                            validators=[DataRequired()])
    course = SelectField("Course", choices=[])
    year_level = SelectField("Year Level", choices=[1, 2, 3, 4, 5])
    gender = SelectField("Gender",
                         choices=["Male", "Female"])
    profile_pic = FileField("Upload a Profile Picture",
                                validators=[FileAllowed(["png", "jpg", "jpeg"])])
    add = SubmitField("Add")

class SearchForm(FlaskForm):
    search_by = SelectField("Search by",
                            choices=["ID Number", "First name",
                                     "Last name", "Course",
                                     "Year Level", "Gender"])
    this = StringField("This", validators=[DataRequired()])
    search = SubmitField("Search")