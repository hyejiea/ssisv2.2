from ssims import my_sql
from ssims.colleges.forms import CollegeForm
from ssims.colleges.forms import CollegeSearchForm

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
)

college = Blueprint("college", __name__)

@college.route("/colleges")

def colleges():
    connection = my_sql.connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM College")
    colleges = cursor.fetchall()
    form = CollegeSearchForm()

    return render_template("colleges.html", 
                            title="Colleges", 
                            colleges=colleges,form=form)

@college.route("/add_a_college", methods=["POST", "GET"])

def add_a_college():
    form = CollegeForm()

    if request.method == "POST" and form.validate_on_submit():
        college_code = form.college_code.data
        college_name = form.college_name.data

        connection = my_sql.connect()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO College 
            VALUES (%s, %s)""",
            (college_code, college_name))
        connection.commit()

        flash("College {} has been added successfully.".format(form.college_code.data), 
              "success")
        return redirect(url_for("college.colleges"))

    return render_template("add_a_college.html", 
                            title="Add a College", 
                            legend="Add a College", 
                            form=form)

@college.route("/update_a_college/<college_code>", methods=["POST", "GET"])

def update_a_college(college_code):
    form = CollegeForm()

    connection = my_sql.connect()
    cursor = connection.cursor()

    if form.validate_on_submit():
        college_code = form.college_code.data
        college_name = form.college_name.data

        cursor.execute("""
            UPDATE College 
            SET college_code = %s,
                college_name = %s 
                WHERE college_code = %s
            """, (college_code, college_name, college_code)
        )
        connection.commit()

        flash("College {}'s records have been updated successfully.".format(college_code), 
              "success")
        return redirect((url_for("college.colleges")))

    elif request.method == "GET":
        cursor.execute("""
            SELECT * FROM College 
            WHERE college_code = %s""", 
            (college_code))
        college = cursor.fetchone()

        form.college_code.data = college[0]
        form.college_name.data = college[1]
        form.add.label.text = "Update"

    return render_template("add_a_college.html", 
                            title="Update College Records", 
                            legend="Update College Records", 
                            form=form)

@college.route("/delete_a_college/<college_code>", methods=["POST", "GET"])

def delete_a_college(college_code):
    connection = my_sql.connect()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            DELETE FROM College 
            WHERE college_code = %s""", 
            (college_code,))
        connection.commit()

        flash("College {} has been deleted successfully.".format(college_code), 
            "danger")
    except:
        flash("You are not allowed to delete this college.", 
            "warning")
    return redirect((url_for("college.colleges")))

@college.route("/college_search", methods=["POST", "GET"])
def college_search():
    form = CollegeSearchForm()

    pairs = {
        "College code": "college_code",
        "College name": "college_name"
    }

    connection = my_sql.connect()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM College WHERE {} = %s".format(pairs[form.search_by.data]),
                   (form.this.data))
    colleges = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("colleges.html", title="Colleges", 
                            colleges=colleges, form=form)

