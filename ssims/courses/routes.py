from ssims import my_sql
from ssims.courses.forms import CourseForm
from ssims.courses.forms import CourseSearchForm

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)

course = Blueprint("course", __name__)

@course.route("/courses")

def courses():
    connection = my_sql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Course")
    courses = cursor.fetchall()
    form = CourseSearchForm()

    return render_template("courses.html", 
                            title="Courses", 
                            courses=courses,form=form)

@course.route("/add_a_course", methods=["POST", "GET"])

def add_a_course():
    form = CourseForm()

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT college_code FROM College")
    colleges = cursor.fetchall()
    form.college.choices = [college[0] for college in colleges]

    if request.method == "POST" and form.validate_on_submit():
        course_code = form.course_code.data
        course_name = form.course_name.data
        college = form.college.data

        cursor.execute("""
            INSERT INTO Course 
            VALUES (%s, %s, %s)""",
            (course_code, course_name, college))
        connection.commit()

        flash("Course {} has been added successfully.".format(form.course_code.data), 
              "success")
        return redirect(url_for("course.courses"))

    return render_template("add_a_course.html", 
                            title="Add a Course", 
                            legend="Add a Course", 
                            form=form)

@course.route("/delete_a_course/<course_code>", methods=["POST", "GET"])

def delete_a_course(course_code):
    connection = my_sql.connect()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            DELETE FROM Course 
            WHERE course_code = %s""", 
            (course_code,))
        connection.commit()

        flash("Course {} has been deleted successfully.".format(course_code), 
            "danger")
    except:
        flash("You are not allowed to delete this course.", 
            "warning")
    return redirect((url_for("course.courses")))

@course.route("/update_a_course/<course_code>", methods=["POST", "GET"])

def update_a_course(course_code):
    form = CourseForm()

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT college_code FROM College")
    colleges = cursor.fetchall()
    form.college.choices = [college[0] for college in colleges]

    if form.validate_on_submit():
        course_code = form.course_code.data
        course_name = form.course_name.data
        college = form.college.data

        cursor.execute("""
            UPDATE Course 
            SET course_code = %s,
                course_name = %s,
                college = %s
                WHERE course_code = %s
            """, (course_code, course_name, college, course_code)
        )
        connection.commit()

        flash("Course {}'s records have been updated successfully.".format(course_code), 
              "success")
        return redirect((url_for("course.courses")))

    elif request.method == "GET":
        cursor.execute("""
            SELECT * FROM Course 
            WHERE course_code = %s""", 
            (course_code))
        course = cursor.fetchone()

        form.course_code.data = course[0]
        form.course_name.data = course[1]
        form.college.data = course[2]
        form.add.label.text = "Update"

    return render_template("add_a_course.html", 
                            title="Update Course Records", 
                            legend="Update Course Records", 
                            form=form)

@course.route("/course_search", methods=["POST", "GET"])
def course_search():

    form = CourseSearchForm()

    pairs = {
        "Course code": "course_code",
        "Course name": "course_name",
        "College": "college"
    }

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Course WHERE {} = %s".format(pairs[form.search_by.data]),
                   (form.this.data))
    courses = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("courses.html", title="Courses", 
                            courses=courses, form=form)