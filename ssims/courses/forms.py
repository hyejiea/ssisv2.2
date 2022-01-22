from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    StringField,
    SubmitField
)
from wtforms.validators import DataRequired

class CourseForm(FlaskForm):
    course_code = StringField("Course code",
                                render_kw={"placeholder": "Course Code"},
                                validators=[DataRequired()])
    course_name = StringField("Course name",
                                render_kw={"placeholder": "Course Name"},
                                validators=[DataRequired()])
    college = SelectField("College", choices=[])
    add = SubmitField("Add")

class CourseSearchForm(FlaskForm):
    search_by = SelectField("Search by", 
                            choices=["Course code", 
                                     "Course name",
                                     "College"])
    this = StringField("This", validators=[DataRequired()])
    search = SubmitField("Search")
