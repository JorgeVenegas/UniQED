from flask import redirect, session, render_template
from functools import wraps

def apology(message, code=400):
    def escape(s):
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", session=session, code=code, message=escape(message)), code

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def no_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is not None:
            return redirect("/home")
        return f(*args, **kwargs)
    return decorated_function

######### FUNCTIONS CREATED TO REGISTER MASIVE NUMBER OF STUDENTS JUST FOR PRESENTATION
def quicksignup():
    line_count = 0
    cid = "CS50AI-1"
    with open('static/rdta.csv', mode='r') as csv_file:
        data = csv.DictReader(csv_file, delimiter=',')
        for row in data:
            if line_count == 0:
                line_count += 1
            username = row['username']

            # Register new user into database
            users = db.execute("SELECT id FROM users WHERE username = ?", username)
            user_id = users[0]['id']

            # Search if course exits in database
            course = db.execute("SELECT * FROM courses WHERE id=?", cid)

            # Search for availability in desired course.
            if not course[0]['remaining']  > 0:
                break

            # Add course enrollment
            db.execute("UPDATE courses SET remaining = remaining - 1 WHERE id = ?", cid)
            db.execute("INSERT INTO enrrollments (student_id, course_id) VALUES (?, ?)", user_id, course[0]['id'])

            lessons = db.execute("SELECT * FROM lessons WHERE course_id = ?", cid)

            for lesson in lessons:
                db.execute("INSERT INTO progress (student_id, course_id, chapter_id, lesson_id) VALUES (?, ?, ?, ?)", user_id, cid, lesson['chapter_id'], lesson['lesson_id'])


def randomstatus():
    enrollments = db.execute("SELECT lesson_id FROM enrrollments")
    seed(1)
    status = {1 : "Excellent", 2 : "Good", 3 : "Needs Attention"}
    for enrollment in enrollments:
        x = randint(1, 3)
        db.execute("UPDATE enrrollments SET status = ? WHERE enrollment_id = ?", status[x], enrollment['enrollment_id'])

def randomprogressstatus():
    lessons = db.execute("SELECT * FROM progress")
    seed(1)
    status = {1 : "Completed", 2 : "Incomplete"}
    for lesson in lessons:
        x = randint(1, 2)
        db.execute("UPDATE progress SET status = ? WHERE lesson_id = ?", status[x], lesson['lesson_id'])

    enrollments = db.execute("SELECT * FROM enrrollments")
    for enrollment in enrollments:

        # Looks for the total number of lessons
        total = db.execute("SELECT COUNT(*) AS total FROM progress WHERE course_id = ? and student_id = ?", enrollment['course_id'], enrollment['student_id'])
        total = total[0]['total']

        # Looks for the number of lessons completed
        completed = db.execute("SELECT COUNT(*) AS completed FROM progress WHERE course_id = ? AND student_id = ? AND status = 'Completed'", enrollment['course_id'], enrollment['student_id'])
        completed = completed[0]['completed']

        # Defines de progress of the course overall with an integer percentage
        if total != 0:
            progress = int(completed / total * 100)
        else:
            progress = 0

        # Sets the progress for the current enrollment
        db.execute("UPDATE enrrollments SET progress = ? WHERE student_id = ? AND course_id = ?", progress, enrollment['student_id'], enrollment['course_id'])


def correctgender():
    db.execute("UPDATE users SET gender = 'female' WHERE gender = 'Female'")
    db.execute("UPDATE users SET gender = 'male' WHERE gender = 'Male'")