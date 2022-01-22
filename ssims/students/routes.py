from ssims import my_sql
from ssims.students.forms import StudentForm
from ssims.students.forms import SearchForm
from cloudinary.uploader import upload, destroy
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)

student = Blueprint("student", __name__)

@student.route("/students", methods=["POST", "GET"])
@student.route("/", methods=["POST", "GET"])
def students():
    connection = my_sql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    form = SearchForm()

    return render_template("students.html",
                            title="Students",
                            students=students,form=form)

@student.route("/delete/<id_number>", methods=["POST", "GET"])
def delete(id_number):
    connection = my_sql.connect()
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM Student 
        WHERE id_number = %s""", 
        (id_number,))
    connection.commit()

    destroy(public_id="ssims-flask/{}".format(id_number))

    flash("Student {}'s records have been deleted successfully.".format(id_number), 
          "danger")
    return redirect((url_for("student.students")))

@student.route("/add_a_student", methods=["POST", "GET"])
def add_a_student():

    form = StudentForm()

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT course_code FROM Course")
    courses = cursor.fetchall()
    form.course.choices = [course[0] for course in courses]

    if request.method == "POST" and form.validate_on_submit():
        id_number = form.id_number.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        course = form.course.data
        year_level = form.year_level.data
        gender = form.gender.data
        profile_pic = form.profile_pic.data
        profile_pic = upload(profile_pic.read()).get('url')

        cursor.execute("""
            INSERT INTO Student 
            VALUES (%s, %s, %s, %s, %s, %s,%s)""",
            (id_number, first_name, last_name, course, year_level, gender,profile_pic))
        connection.commit()

        flash("Student {} has been added successfully.".format(form.id_number.data), 
              "success")
        return redirect(url_for("student.students"))

    return render_template("add_a_student.html",
                            title="Add a Student",
                            legend="Add a Student",
                            form=form)

@student.route("/update/<id_number>", methods=["POST", "GET"])
def update(id_number):
    form = StudentForm()

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT course_code FROM Course")
    courses = cursor.fetchall()
    form.course.choices = [course[0] for course in courses]

    if form.validate_on_submit():
        id_number = form.id_number.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        course = form.course.data
        year_level = form.year_level.data
        gender = form.gender.data
        profile_pic = form.profile_pic.data
        profile_pic = upload(profile_pic.read()).get('url')

        cursor.execute("""
            UPDATE Student
            SET id_number = %s,
                first_name = %s,
                last_name = %s,
                course = %s,
                year_level = %s,
                gender = %s,
                profile_pic=%s
                WHERE id_number = %s
            """, (id_number, first_name, last_name, course, year_level, gender, profile_pic, id_number)
        )
        connection.commit()

        flash("Student {}'s records have been updated successfully.".format(id_number), 
              "success")
        return redirect((url_for("student.students")))

    elif request.method == "GET":
        cursor.execute("""
        SELECT * FROM Student 
        WHERE id_number = %s""", 
        (id_number))
        student = cursor.fetchone()

        form.id_number.data = student[0]
        form.first_name.data = student[1]
        form.last_name.data = student[2]
        form.course.data = student[3]
        form.year_level.data = student[4]
        form.gender.data = student[5]
        form.add.label.text = "Update"

    return render_template("add_a_student.html",
                            title="Update Student Records",
                            legend="Update Student Records",
                            form=form)

@student.route("/search", methods=["POST", "GET"])
def search():
    form = SearchForm()

    pairs = {
        "ID Number": "id_number",
        "First name": "first_name",
        "Last name": "last_name",
        "Course": "course",
        "Year Level": "year_level",
        "Gender": "gender"
    }

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Student WHERE {} = %s".format(pairs[form.search_by.data]),
                   (form.this.data))
    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("students.html", title="Students",
                            students=students,form=form)