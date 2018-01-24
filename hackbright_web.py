"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, flash, redirect

import hackbright

app = Flask(__name__)
app.secret_key = 'this-should-be-something-unguessable'


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    projects = hackbright.get_grades_by_github(github)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           projects=projects)

    return html
    # return "{acct} is the GitHub account for {first} {last}".format(
    #     acct=github, first=first, last=last)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-create", methods=['GET'])
def student_create():
    """Add a student."""

    return render_template("student_create.html")


@app.route("/student-added", methods=['POST'])
def student_added():
    """Process adding a student."""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)
    flash("The student has been successfully added.")
    return redirect("/student-search")


@app.route("/project/<title>")
def get_projects(title):
    """Displays all project names, descriptions and max grades."""

    name, description, max_grade = hackbright.get_project_by_title(title)

    student_grades = hackbright.get_grades_by_title(title)

    return render_template("project_info.html", name=name,
                                                description=description,
                                                max_grade=max_grade,
                                                student_grades=student_grades)


@app.route("/add_project")
def make_project():
    """Add a new project."""

    return render_template("add_project.html")


@app.route("/project_added", methods=['POST'])
def project_added():
    """Process adding a project."""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.add_project(title, description, max_grade)
    flash("The project has been successfully added.")
    return redirect("/home")


@app.route("/add_grades")
def grade_student_project():

    students = hackbright.get_students()
    print students
    projects = hackbright.get_projects()

    return render_template("assign_grades.html", 
                           students=students, 
                           projects=projects)


@app.route("/assign_grades", methods=['POST'])
def assign_grades_project():

    github = request.form.get('github')
    project = request.form.get('project')
    grade = request.form.get('grade')

    hackbright.assign_grade(github, project, grade)
    flash("The student's grade has been successfully added.")
    return redirect("/home")



@app.route("/home")
def display_all():

    students = hackbright.get_students()
    projects = hackbright.get_projects()

    return render_template("homepage.html", students=students, projects=projects)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
