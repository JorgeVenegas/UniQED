import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from helpers import login_required, no_login_required, apology
from werkzeug.security import check_password_hash, generate_password_hash

from random import seed
from random import randint

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///uniqed.db")

@app.route("/")
@no_login_required
def index():
    # lol()
    return render_template("index.html")

@app.route("/signup/", methods=["GET", "POST"])
@no_login_required
def signup():
    if request.method == "POST":

        # Get data from the submitted form
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        age = request.form.get("age")
        gender = request.form.get("gender")
        email = request.form.get("email")
        language = request.form.get("language")
        phone = request.form.get("phone")
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("roleRadio")

        # Look for existing username
        users = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Chek if user is already registered
        if len(users) != 0:
            return apology("Invalid request. Already registered", 400)

        # Register new user into database
        db.execute("INSERT INTO users (fname, lname, age, gender, email, language, phone, username, hash, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", fname, lname, age, gender, email, language, phone, username, generate_password_hash(password), role)

        return redirect("/login")
    else:
        return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
@no_login_required
def login():
    if request.method == "POST":

        # Get data from the submitted form
        username = request.form.get("username")
        password = request.form.get("password")

        # Look for credentials in database
        users = db.execute("SELECT id, fname, lname, username, hash, role FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(users) != 1 or not check_password_hash(users[0]["hash"], password):
            return apology("Invalid request. Incorrect credentials", 400)

        # Get the first and only user of the user's list
        user = users[0]

        # Set session variables with important data
        session["logged_in"] = True
        session["user_id"] = user["id"]
        session['username'] = user['username']
        session['fname'] = user['fname']
        session['lname'] = user['lname']
        session['role'] = user['role']

        return redirect("/home")
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():

    # Forget any user_id
    session.clear()

    return redirect("/")

@app.route("/home")
@login_required
def home():

    # Search for events and notes of the user logged in
    events = db.execute('SELECT * FROM events WHERE user_id=? ORDER BY date', session['user_id'])
    notes = db.execute('SELECT * FROM notes WHERE user_id=? ORDER BY date DESC', session['user_id'])

    # Render home template according to user's role
    if session['role'] == 'student':
        return render_template_logged_in("homeStudent.html", events=events, notes=notes)
    elif session['role'] == 'teacher':
        return render_template_logged_in("homeTeacher.html", events=events, notes=notes)
    else:
        # Handle different session role with an apology
        return apology("Error handling your request. Try again.", 400)

@app.route("/agenda")
@login_required
def agenda():

    # Search for events of the user logged in in database
    events = db.execute('SELECT * FROM events WHERE user_id=? ORDER BY date', session['user_id'])

    return render_template_logged_in("agenda.html", events=events)

@app.route("/notes")
@login_required
def notes():

    # Search for notes of the user logged in in database
    notes = db.execute('SELECT * FROM notes WHERE user_id=? ORDER BY date', session['user_id'])

    return render_template_logged_in("notes.html", notes=notes)

@app.route("/create/<obj>", methods=['POST'])
@login_required
def create(obj):

	# Handling the creation of a new course
    if obj == 'courses':
        key = request.form.get('key')
        section = request.form.get('section')
        name = request.form.get('name')
        size = request.form.get('size')
        language = request.form.get('language')

        cid = key + '-' + section
        teacher = session['user_id']

        # Looks for course in database
        courses = db.execute("SELECT * FROM courses WHERE id=?", cid)

        # If course already exists renders apology
        if not len(courses) == 0:
            return apology("Invalid request. Course already exists.", 400)

        # Inserts new course info into database
        db.execute("INSERT INTO courses (id, key, section, name, teacher_id, available, remaining, language) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", cid, key, section, name, teacher, size, size, language)
    else:
        return apology('Invalid request. Try again.', 400)

    return redirect('/home')

@app.route("/add/<obj>", methods=['POST'])
@login_required
def add(obj):

    # Handling the addtition of a new course. Only for student users
    if obj == 'courses':
        cid = request.form.get('id')

        # Search if course exits in database
        course = db.execute("SELECT * FROM courses WHERE id=?", cid)
        if not len(course) == 1:
            return apology("Invalid request. Course does not exists", 400)

        # Search if user is already enrolled in desired course
        if len(db.execute("SELECT * FROM enrrollments WHERE ? IN (SELECT course_id FROM enrrollments WHERE student_id = ?)", cid, session['user_id'])) > 0:
            return apology("Invalid request. Already registered.", 400)

        # Search for availability in desired course.
        if not course[0]['remaining']  > 0:
            return apology("Not enough seats available", 400)

        # Add course enrollment
        db.execute("UPDATE courses SET remaining = remaining - 1 WHERE id = ?", cid)
        db.execute("INSERT INTO enrrollments (student_id, course_id) VALUES (?, ?)", session['user_id'], course[0]['id'])

        lessons = db.execute("SELECT * FROM lessons WHERE course_id = ?", cid)

        for lesson in lessons:
            db.execute("INSERT INTO progress (student_id, course_id, chapter_id, lesson_id) VALUES (?, ?, ?, ?)", session['user_id'], cid, lesson['chapter_id'], lesson['lesson_id'])

    # Handling the addtition of a new event
    elif obj == 'events':
        title = request.form.get('eventTitle')
        date = request.form.get('eventDate')
        time = request.form.get('eventTime')
        description = request.form.get('eventDescription')

        db.execute("INSERT INTO events (user_id, title, date, time, description) VALUES (?, ?, ?, ?, ?)", session['user_id'], title, date, time, description)

    # Handling the addtition of a new note
    elif obj == 'notes':
        title = request.form.get('noteTitle')
        description = request.form.get('noteDescription')

        db.execute("INSERT INTO notes (user_id, title, description) VALUES (?, ?, ?)", session['user_id'], title, description)
    else:
        return apology("Invalid request. Try again", 400)

    return redirect('/home')

@app.route("/delete/<obj>/<int:id>", methods=['POST'])
@login_required
def delete(obj, id):

    # Handles the deletion of events and notes
    if obj == 'events':
        db.execute("DELETE FROM events WHERE id=?", id)
    elif obj == 'notes':
        db.execute("DELETE FROM notes WHERE id=?", id)
    else:
        return apology("Invalid request. Try again", 400)

    return redirect('/home')

@app.route("/course/<cid>")
@login_required
def course(cid):
    if session['role'] == 'student':

        # Looks for all the updated data accordign to the specified enrollment
        enrollments = db.execute("SELECT * FROM enrrollments WHERE student_id = ? AND course_id = ?", session['user_id'], cid)
        enrollment = enrollments[0]

        # Looks for the chapters and lessons for the corresponding course
        chapters = db.execute('SELECT * FROM chapters WHERE course_id = ?', cid)
        for chapter in chapters:
            # Looks for the number of lessons completed within the chapter
            completed = db.execute("SELECT COUNT(*) AS completed FROM progress WHERE chapter_id = ? AND student_id = ? AND status = 'Completed'", chapter['chapter_id'], session['user_id'])
            chapter['completed'] = completed[0]['completed']
            chapter['lessons'] = db.execute('SELECT * FROM lessons WHERE chapter_id = ? ORDER BY lesson_id ASC', chapter['chapter_id'])

        return render_template_logged_in('courseOverviewStudent.html', enrollment=enrollment, chapters=chapters)

    elif session['role'] == 'teacher':
        # Looks for the current course data
        courses = db.execute('SELECT * FROM courses WHERE teacher_id = ? AND id = ?', session['user_id'], cid)
        course = courses[0]

        # Looks and categorizes status data form students enrolled in the course
        status = {}
        excellent = db.execute("SELECT COUNT(status) AS status FROM enrrollments WHERE course_id = ? AND status = 'Excellent'", cid)
        status['excellent'] = excellent[0]['status']
        good = db.execute("SELECT COUNT(status) AS status FROM enrrollments WHERE course_id = ? AND status = 'Good'", cid)
        status['good'] = good[0]['status']
        attention = db.execute("SELECT COUNT(status)  AS status FROM enrrollments WHERE course_id = ? AND status = 'Needs Attention'", cid)
        status['attention'] = attention[0]['status']

        # Looks and categorizes stats data form students enrolled in the course
        stats = {}
        progress = db.execute("SELECT AVG(progress) AS progress FROM enrrollments WHERE course_id = ?", cid)
        stats['progress'] = progress[0]['progress']
        male = db.execute("SELECT COUNT(gender) AS gender FROM users WHERE gender = 'male' AND id IN (SELECT student_id FROM enrrollments WHERE course_id = ?)", cid)
        female = db.execute("SELECT COUNT(gender) AS gender FROM users WHERE gender = 'female' AND id IN (SELECT student_id FROM enrrollments WHERE course_id = ?)", cid)
        male = male[0]['gender']
        female = female[0]['gender']
        if male == 0 and female == 0:
            stats['relation'] = str(0) + "%/" + str(0) + "%"
        else:
            stats['relation'] = str(int(100 * male / (male + female))) + "%/" + str(int(100 * female / (male + female))) + "%"

        # Looks for the chapters and lessons for the corresponding course
        chapters = db.execute('SELECT * FROM chapters WHERE course_id = ?', cid)
        for chapter in chapters:
            chapter['lessons'] = db.execute('SELECT * FROM lessons WHERE course_id = ? AND chapter_id = ? ORDER BY lesson_id ASC', cid, chapter['chapter_id'])

        # Looks for the students enrolled in the course
        students = db.execute("SELECT * FROM users u INNER JOIN enrrollments e ON u.id=e.student_id WHERE course_id = ? ORDER BY fname ASC", cid)

        return render_template_logged_in('courseOverviewTeacher.html', course=course, status=status, stats=stats, chapters=chapters, students=students)

@app.route("/course/<cid>/chapter/<int:chid>")
@login_required
def course_chapter(cid, chid):

    # Looks for the total number of lessons
    total = db.execute("SELECT COUNT(*) AS total FROM lessons WHERE chapter_id = ?", chid)
    total = total[0]['total']

    # Looks for the number of lessons completed
    completed = db.execute("SELECT COUNT(*) AS completed FROM progress WHERE chapter_id = ? AND student_id = ? AND status = 'Completed'", chid, session['user_id'])
    completed = completed[0]['completed']

    # Defines de progress of the chapter overall with an integer percentage
    if total != 0:
        progress = int(completed / total * 100)
    else:
        progress = 0

	# Looks for all the updated data accordign to the specified enrollment
    enrollments = db.execute("SELECT * FROM enrrollments WHERE student_id = ? AND course_id = ?", session['user_id'], cid)
    enrollment = enrollments[0]

    # Looks for the specified chapter and lessons for the corresponding course
    chapters = db.execute('SELECT * FROM chapters WHERE course_id = ? AND chapter_id = ?', cid, chid)
    chapter = chapters[0]
    chapter['progress'] = progress
    lessons = db.execute('SELECT * FROM lessons l INNER JOIN progress p ON l.lesson_id=p.lesson_id WHERE l.course_id = ? AND l.chapter_id = ? AND student_id = ? ORDER BY lesson_id ASC', cid, chid, session['user_id'])

    return render_template_logged_in('chapterOverviewStudent.html', enrollment=enrollment, chapter=chapter, lessons=lessons)

@app.route("/course/<cid>/chapter/<int:chid>/lessonCompleted/<int:lid>", methods=['POST'])
@login_required
def set_lesson_completed(cid, chid, lid):

    # Sets specifed lesson's status as completed
    db.execute("UPDATE progress SET status = 'Completed' WHERE course_id = ? AND chapter_id = ? AND lesson_id = ? AND student_id = ?", cid, chid, lid, session['user_id'])

    # Looks for the total number of lessons
    total = db.execute("SELECT COUNT(*) AS total FROM progress WHERE course_id = ? and student_id = ?", cid, session['user_id'])
    total = total[0]['total']

    # Looks for the number of lessons completed
    completed = db.execute("SELECT COUNT(*) AS completed FROM progress WHERE course_id = ? AND student_id = ? AND status = 'Completed'", cid, session['user_id'])
    completed = completed[0]['completed']

    # Defines de progress of the course overall with an integer percentage
    if total != 0:
        progress = int(completed / total * 100)
    else:
        progress = 0

    # Sets the progress for the current enrollment
    db.execute("UPDATE enrrollments SET progress = ? WHERE student_id = ? AND course_id = ?", progress, session['user_id'], cid)

    return redirect(url_for('course_chapter', cid=cid, chid=chid))

@app.route("/course/<cid>/<name>")
@login_required
def course_student(cid, name):

    # Looks for specified course
    courses = db.execute('SELECT * FROM courses WHERE teacher_id = ? AND id = ?', session['user_id'], cid)
    course = courses[0]

    # looks for specified student
    students = db.execute("SELECT * FROM users u INNER JOIN enrrollments e ON u.id=e.student_id WHERE u.fname = ? AND e.course_id = ? ", name,  cid)
    student = students[0]

    return render_template_logged_in('studentOfCourseOverview.html', course=course, student=student)

@app.route("/course/<cid>/addChapter", methods=['POST'])
@login_required
def add_chapter(cid):

    # Get data from the submitted form
    number = request.form.get('chapterNumber')
    title = request.form.get('chapterTitle')
    description = request.form.get('chapterDescription')

    # Handles chapter addition to course in database
    db.execute("INSERT INTO chapters (course_id, chapter_id, title, description) VALUES (?, ?, ?, ?)", cid, number, title, description)

    return redirect(url_for('course', cid=cid))

@app.route("/course/<cid>/<chid>/addLesson", methods=['POST'])
@login_required
def add_lesson(cid, chid):

    # Get data from the submitted form
    title = request.form.get('lessonTitle')
    number = request.form.get('lessonNumber')
    content = request.form.get('lessonContent')

    # Handles lesson addition to chapter in database
    db.execute("INSERT INTO lessons (course_id, chapter_id, lesson_id, title, content) VALUES (?, ?, ?, ?, ?)", cid, chid, number, title, content)


    enrollments = db.execute("SELECT student_id FROM enrrollments WHERE course_id = ?", cid)

    # Updates the progress of the course enrollments
    for enrollment in enrollments:
        db.execute("INSERT INTO progress (student_id, course_id, chapter_id, lesson_id) VALUES (?, ?, ?, ?)", enrollment['student_id'], cid, chid, number)

        # Looks for the total number of lessons
        total = db.execute("SELECT COUNT(DISTINCT(lesson_id)) AS total FROM progress WHERE course_id = ? AND student_id = ?", cid, enrollment['student_id'])
        total = total[0]['total']
        print("Student ID: " + str(enrollment['student_id']) + ", Total: " + str(total))

        # Looks for the number of lessons completed
        completed = db.execute("SELECT COUNT(*) AS completed FROM progress WHERE course_id = ? AND student_id = ? AND status = 'Completed'", cid, enrollment['student_id'])
        completed = completed[0]['completed']
        print("Student ID: " + str(enrollment['student_id']) + ", Completed: " + str(completed))

        # Defines de progress of the course overall with an integer percentage
        if total != 0:
            progress = int(completed / total * 100)
        else:
            progress = 0

        print("Student ID: " + str(enrollment['student_id']) + ", Progress: " + str(progress))

        # Sets the progress for the current enrollment
        db.execute("UPDATE enrrollments SET progress = ? WHERE student_id = ? AND course_id = ?", progress, enrollment['student_id'], cid)

    return redirect(url_for('course', cid=cid))

@app.route("/updateStatus/<int:eid>", methods=['POST'])
@login_required
def update_status(eid):

    # Gets specified status and updates in in the database
    status = request.form.get('statusRadio')
    db.execute("UPDATE enrrollments SET status = ? WHERE enrollment_id = ?", status, eid)

    # Gets data about the current enrollment bing manipulation for redirection
    enrrollments =db.execute("SELECT * FROM users u INNER JOIN enrrollments e ON u.id=e.student_id WHERE enrollment_id = ?", eid)
    enrrollment = enrrollments[0]

    # Sets arguments for redirect function
    cid = enrrollment['course_id']
    name = enrrollment['fname']

    return redirect(url_for('course_student', cid=cid, name=name))

def render_template_logged_in(template, **args):

    if session['role'] == 'student':
        courses = db.execute('SELECT c.*, t.fname, t.lname FROM courses c INNER JOIN users t ON c.teacher_id=t.id WHERE c.id IN (SELECT course_id FROM enrrollments WHERE student_id=?) ', session['user_id'])
    elif session['role'] == 'teacher':
        courses = db.execute('SELECT * FROM courses WHERE teacher_id=? ORDER BY id', session['user_id'])

    return render_template(template, **args, session=session, courses=courses)