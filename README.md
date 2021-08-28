# UniQEd

#### Video Demo:

[Youtube link to video](https://youtu.be/FT2Yf10bpkA).


#### Description:

### Summary

UniQEd is a web -based application developed using HTML, CSS, Javascript and Bootstrap for the Front-end, and Python(Flask) and SQL for the Back-end. This application is intended to be a prototype for an online learning platform based on personalized learning.

### Structure and HTML Templates Layouts

Since it has been developed with Flask, the structure of the project is defined by Flask's structure, having the "static" directory, the "templates" directory,.and the python application files within the application directory. Starting with the "templates" directory, the UniQEd platform has 2 different layouts used with different purposes:

- `layout.html`: Designed for the landing page and its main sections (Home, Sign Up, Log In)
- `layoutHome.html`: Designed for the homepage and everything else displayed whenever a user is logged into the site.

### Application States, Main Features and Main HTML Templates

The application can be used by 2 different type of users: students and teachers; therefore, it renders different templates  and data for each of them. Being this said, the application can have 3 different states that dictate which HTML templates might be used and when:

- Not user logged in: First state of the application, happening whenever there is not user logged in. For this state the layout used is `layout.html`, which is also used by another 3 templates:

  1. `index.html`: Where the user has his first approach to the platform and its objective through the landing page.

  2. `signup.html`: Where the user can register himself in order to access the main features of the application.

  3. `login.html`: Where the user gives his credentials previously registered to access his personalized homepage.

- User logged in: This state has 4 main features regardless of the user's role:

  1. Show the homepage with personalized data.
  2. Show each user courses' overview..
  3. Show each user's agenda.
  4. Show each user's notes.

  This state is divided into de other 2 states according to the user's role. For this 2 states the layout used is `layoutHome.html` since both will require a user to be logged in:

  - Logged in as a Teacher: The second state of the application, happening whenever a user is logged in with the role of *teacher*. The templates used for this state are:
    1. `homeTeacher.html`: Where the teacher can view his homepage and all the data presented on it. (Main feature 1)
    2. `courseOverviewTeacher.html`: Where the teacher can view each course overview. (Main feature 2)
    3. `agenda.html`: Where the teacher can view his agenda. (Main feature 3)
    4. `notes.html`: Where the teacher can view his notes. (Main feature 4)
    5. `studentOfCourseOverview.html`: Where the teacher can have a closer look of an specific student of a specific course.
  - Logged in as a Student: The third and last state of the application, happening whenever a user is logged in with the role of *student*.  The templates used for this state are:
    1. `homeStudent.html`: Where the student can view his homepage and all the data presented on it. (Main feature 1)
    2. `courseOverviewStudent.html`: Where the student can view each course overview. (Main feature 2)
    3. `agenda.html`: Where the student can view his agenda. (Main feature 3)
    4. `notes.html`: Where the student can view his notes. (Main feature 4)
    5. `chapterOverviewStudent.html`: Where the student can have a closer look of an specific chapter of a specific course.

- Finally, we have another template: `apology.html`, which works as an error handler.

### CSS and JavaScript Functionality

In the *static* directory the application has 2 files:

1. `styles.css`: For all the styles applied in the application. This file might be slightly short since the majority of styles used come from *Boostrap* and its predefined classes.

2. `main.js`: For all the event listeners of the application (modals, accordions, etc), as well as some specific functions used throughout the project. Some examples of the usage of Javascript within the project are:

   - Adding or removing classes to the `nav` or `sidebar` according to the actual page being rendered:

     ```javascript
     var nav = document.getElementById("navbar-nav");
     var navlinks = nav.getElementsByClassName("nav-link");
     var current = document.getElementById("current")

     for (var i = 0; i < navlinks.length; i++) {
       if (navlinks[i].innerHTML == current.innerHTML) {
         navlinks[i].className += " active";
       }
     };
     ```

     ```javascript
     var sidebar = document.getElementById("sidebar");

     if (sidebar != null) {
       var sidebarlinks = sidebar.getElementsByClassName("nav-link");

       var actual = document.getElementById("actual")

       if (actual != null) {
         for (var i = 0; i < sidebarlinks.length; i++) {

           if (sidebarlinks[i].getAttribute('data-bs-name') == actual.innerHTML) {
             sidebarlinks[i].className += " active";
           }
         };
       }
     }
     ```

   - Setting al the forms `autocomplete` property to off to avoid  it at every moment.

     ```javascript
     let forms = document.getElementsByTagName("form");

     for (let i = 0; i < forms.length; i++) {
       forms[i].autocomplete = "off";
     }
     ```

   - Personalizing the information showed in a modal.

     ```javascript
     var eventDescriptionModal = document.getElementById('eventDescriptionModal')

     if (eventDescriptionModal != null) {
       eventDescriptionModal.addEventListener('show.bs.modal', function (event) {
         var button = event.relatedTarget;

         var id = button.getAttribute('data-bs-id');

         var title = document.getElementById('eventTitle' + id);
         var date = document.getElementById('eventDate' + id);
         var time = document.getElementById('eventTime' + id);
         var description = document.getElementById('eventDescription' + id);

         var eventTitle = eventDescriptionModal.querySelector('.eventModalTitle');
         var eventDate = eventDescriptionModal.querySelector('.eventModalDate');
         var eventTime = eventDescriptionModal.querySelector('.eventModalTime');
         var eventDescription = eventDescriptionModal.querySelector('.eventModalDescription');

         eventTitle.textContent = title.innerHTML;
         eventDate.textContent = date.innerHTML;
         eventTime.textContent = time.innerHTML;
         eventDescription.textContent = description.innerHTML;

         document.getElementById('deleteEvent').setAttribute('action', "/delete/events/" + id);
       })
     }
     ```

   - Adding and removing classes to accordions to style them

     ```javascript
     var lessonsAccordion = document.getElementById('lessons')

     if (lessonsAccordion != null) {
       var firstLesson = lessonsAccordion.querySelector("button")
       var firstLessonCollapsed = lessonsAccordion.querySelector(".accordion-collapse")

       firstLesson.setAttribute("areia-expandend", "true")

       firstLesson.classList.remove("collapsed")
       firstLessonCollapsed.classList.add("show")
     }
     ```

### Database implementation through SQLite

For storing data the application uses relational databases through SQLite3. UniQEd has 8 tables to manage and store all the information used throughout the whole application.

![](/static/images/Uniqued DB Schema.png)

- `users`: Stores all the data related to the registered users. Here the role of the users is defines, as well as their personal information, username, and hashed password.
- `events`: Stores data of events of all users.
- `notes`: Stores data of notes of all users.
- `courses`: Stores all the data of the created courses, such as the available and remaining seats, the teacher identifier, as well as its language.
- `enrollments`: Stores all the data of the students enrolled in already created courses, such as the progress, status and date of enrollment, etc..
- `chapters`: Stores data of each chapter of each course created, such as its title and description.
- `lessons`: Stores data of each lesson of each chapter of each course created, such as its title, number and content.
- `progress`: Stores data of the status of each lesson each course of each course created, this help determine the overall progress of an enrollment..

The connection of the application to the UniQEd database is established through the following statement

```python
db = SQL("sqlite:///uniqed.db")
```

which is positiones just after the Flask app is initialized within the python main file.

### Python Implementation and Routing

For the proper rendering of data and information the implementation of Flask through Python is needed for the application. Thus, 2 files were created in order to make the application work correctly and as smooth as possible:

- `helpers.py`: Contains 3 functions:

  1. For login required: Helps controlling access to functions at application.py, only giving access if the user is logged in. This function is used in the second and third state of the application.

     ```python
     def login_required(f):
         @wraps(f)
         def decorated_function(*args, **kwargs):
             if session.get("user_id") is None:
                 return redirect("/login")
             return f(*args, **kwargs)
         return decorated_function
     ```

  2. For no login required: Helps controlling access to functions at application.py, only giving access if the user is not logged in. This function is used for the first state of the application.

     ```python
     def no_login_required(f):
         @wraps(f)
         def decorated_function(*args, **kwargs):
             if session.get("user_id") is not None:
                 return redirect("/home")
             return f(*args, **kwargs)
         return decorated_function
     ```

  3. For error messages and response codes.

     ```python
     def apology(message, code=400):
         def escape(s):
             for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                              ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
                 s = s.replace(old, new)
             return s
         return render_template("apology.html", session=session, code=code, message=escape(message)), code
     ```

- `application.py`: File that handles all the routing within the application and the manipulation of the stored and new data. To accomplish al the tasks required by the application it has 17 different routes:

  The most basic routes are the ones handling with the less complex templates, such as:

  1. `index() for /`: Renders the landing page.

     ```python
     @app.route("/")
     @no_login_required
     def index():
         return render_template("index.html")
     ```

  From now on, the routes will  be a bit more complex as forms are introduced and data is starting be manipulated and stored.

  2. signup() for /signup: Renders the *sign up* page and handles the *sign up* form submission, storing the registered user in the database and redirecting to the *log in* page.

     ```python
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
     ```

  3. `login() for /login`: Renders the *log in* page and handles the *log in* form submission, looking for the given credentials and logging into the homepage if match with database.

     ````python
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
     ````

  4. `logout() for /logout`: Clears session variables when called, logging out the user.

     ```python
     @app.route("/logout")
     @login_required
     def logout():

         # Forget any user_id
         session.clear()

         return redirect("/")
     ```

> The remaining routes correspond to the second and third state of the application, requiring a user to be logged in. Since all these routes render information about the user within the layout, and since the layout is always used at these states, by the time the application was being developed, it started to have some patterns which repeated the same information once and once again.
>
> - For example, these are some of the vatiables used within the `layoutHome.html` template:
>
>   1. To render the first name and username of the user logged in:
>
>      ```html
>      <div class="navbar-nav" id="navbar-nav" style="color: white;">
>          Welcome again,  {{ session['fname'] }}!
>      </div>
>      ```
>
>      ```html
>      <strong>{{ session['username']}}</strong>
>      ```
>
>   2. To render the list of courses the user was registered in:
>
>      ```html
>      <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small ms-5">
>          {% if courses|length > 0 %}
>          	{% for course in courses %}
>          		<li><a href="/course/{{course['id']}}" class="link-dark rounded" style="text-decoration: none;">{{course['id']}}</a></li>
>          	{% endfor %}
>          {% else %}
>          	You have not registered courses.
>          {% endif %}
>      </ul>
>      ```
>
> To properly render this information in every template using the `layoutHome.html` layout, it was indispensable to pass the `session` dictionary and the list of `courses` every single time the templates were rendered:
>
> - For example:
>
>   ```python
>   return render_template("agenda.html", session=session, courses=courses, events=events)
>   ```
>
>   ```python
>   return render_template('courseOverviewStudent.html', session=session, courses=courses, enrollment=enrollment, chapters=chapters)
>   ```
>
>   ```python
>   return render_template('chapterOverviewStudent.html', session=session, courses=courses, enrollment=enrollment, chapter=chapter, lessons=lessons)
>   ```
>
> In order to remove this pattern of repetition from the whole application routes, the function `render_template_logged_in()` was defined as follows:
>
> ```python
> def render_template_logged_in(template, **args):
>
>     # Select course data according to user role
>     if session['role'] == 'student':
> 		courses = db.execute('SELECT c.*, t.fname, t.lname FROM courses c INNER JOIN userst ON c.teacher_id=t.id WHERE c.id IN (SELECT course_id FROM enrrollments WHERE student_id=?) ', session['user_id'])
>     elif session['role'] == 'teacher':
>         courses = db.execute('SELECT * FROM courses WHERE teacher_id=? ORDER BY id', session['user_id'])
>
>     # Render template with keyword arguments given together with session dictionary and courses list
>     return render_template(template, **args, session=session, courses=courses)
> ```


  5. `home() for /home`:Renders the *homepage*, selecting and showing personalized course information according to the user role, as well as displaying his agenda and notes.

     ```python
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
     ```

  6. `agenda() for /agenda`: Renders the events registered for the user regardless of his role.

     ```python
     @app.route("/agenda")
     @login_required
     def agenda():

         # Search for events of the user logged in in database
         events = db.execute('SELECT * FROM events WHERE user_id=? ORDER BY date', session['user_id'])

         return render_template_logged_in("agenda.html", events=events)
     ```

  7. `notes() for /notes`: Renders the notes registered for the user regardless of his role.

     ```python
     @app.route("/notes")
     @login_required
     def notes():

         # Search for notes of the user logged in in database
         notes = db.execute('SELECT * FROM notes WHERE user_id=? ORDER BY date', session['user_id'])

         return render_template_logged_in("notes.html", notes=notes)
     ```

  8. `create() for /create/<obj>`: Handles the creation of a new course. Only works with *POST* method. This route is for teacher users only.

      ```python
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
      ```

  9. `add() for /add/<obj>`: Handles the addition of courses, events and notes. Only works with *POST* method.

      ```python
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
      ```

  10. `delete() for /delete/<obj>/<int:id>`: Handles deleting events and notes. Only works with *POST* method.

      ```python
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
      ```

  11. `course() for /course/<cid>`: Renders the course overview for either teacher or student users. Only works with *POST* method.

      ```python
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
                  chapter['lessons'] = db.execute('SELECT * FROM lessons WHERE chapter_id = ? ORDER BY lesson_id ASC', chapter['chapter_id'])

              # Looks for the students enrolled in the course
              students = db.execute("SELECT * FROM users u INNER JOIN enrrollments e ON u.id=e.student_id WHERE course_id = ?", cid)

              return render_template_logged_in('courseOverviewTeacher.html', course=course, status=status, stats=stats, chapters=chapters, students=students)
      ```

  12. `course_chapter() for /course/<cid>/chapter/<int:chid>`: Renders the chapter overview of a specified course. Only works with *GET* method. This route is for student users only.

      ```python
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
      ```

  13. `set_lesson_completed() for /course/<cid>/chapter/<int:chid>/lessonCompleted/<int:lid>`: Handles the setting of a specific lesson status as completed. Only works with *POST* method.

      ```python
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
      ```

  14. `course_student() for /course/<cid>/<name>`: Renders an overview of a specific student within a specific course enrollment. Only works with *GET* method.

      ```python
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
      ```

  15. `add_chapter() for /course/<cid>/addChapter`: Handles the addition of a new chapter into a specified course. Only works with *POST* method.

      ```python
      @app.route("/course/<cid>/addChapter", methods=['POST'])
      @login_required
      def add_chapter(cid):

          # Get data from the submitted form
          number = request.form.get('chapterNumber')
          title = request.form.get('chapterTitle')

          # Handles chapter addition to course in database
          db.execute("INSERT INTO chapters (course_id, chapter_id, title) VALUES (?, ?, ?)", cid, number, title)

          return redirect(url_for('course', cid=cid))
      ```

  16. `add_lesson() for /course/<cid>/<chapter>/addLesson`: Handles the addition of a new lesson into a specified chapter. Only works with *POST* method.

      ```python
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
      ```

  17. `update_status() for /updateStatus/<int:eid>`: Handles the update of a specified enrollment. Only works with *POST* method

      ```python
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
      ```

### Jinja Implementation

Jinja was used throughout the whole project templates in order to handle lists of data while avoiding repetition within the code. Some examples of the implementation of jinja in the application are:

- The rendering of all the courses a specific student is enrolled into.

  ```html
  <h2 class="display-6 mb-3">My Courses</h1>
          <div class='row courses'>
              {% if courses|length > 0 %}
                  {% for course in courses %}
                  <div class="col-sm-6 col-md-4 col-lg-3 mb-3">
                    <div class="card home-card">
                      <div class="card-body">
                        <div class="row">
                          <div class="col-12">
                              <span class="h4 m-0" id="courseName_{{ course['name']}}">{{ course['name']}}</span>
                          </div>
                          <div class="col-12">
                              <span class="h5 m-0" id="courseId_{{ course['id']}}">{{ course['id']}}</span>
                          </div>
                          <div class="col-12 <mb-2></mb-2>">
                              <span class="h6" id="courseTeacherName_{{ course['id']}}">{{ course['fname']}} {{ course['lname']}}</span>
                          </div>
                          <div class="col-12 d-flex justify-content-end">
                            <form action="/course/{{course['id']}}" method='GET'>
                              <button type="submit" class="btn btn-outline-light" >More...</button>
                            </form>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  {% endfor %}
              {% else %}
                  <div class="col-xs-12">
                    <h6 class="display-10 mb-3">You have not registered courses.</h1>
                  </div>
              {% endif %}
          </div>
  ```

- The creation of 2 nested accordions with chapters and lessons of an specific course. Thanks to this implementation the application is able to render whichever number of courses and lessons are provided without the requirement of changing the HTML template:

  ```html
  <h3 class="h3 mb-3">Curriculum</h3>
          <div class='row mb-5'>
              <div class='col-12'>
                      {% if chapters|length > 0 %}
                        <div class="accordion mb-3" id="chapters">
                          {% for chapter in chapters %}
                            <div class="accordion-item">
                              <h2 class="accordion-header" id="heading{{ chapter['chapter_id'] }}">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{ chapter['chapter_id'] }}" aria-expanded="dalse" aria-controls="collapse{{ chapter['chapter_id'] }}">
                                  Chapter {{ chapter['chapter_id'] }}: {{ chapter['title'] }}
                                </button>
                              </h2>
                              <div id="collapse{{ chapter['chapter_id'] }}" class="accordion-collapse collapse" aria-labelledby="heading{{ chapter['chapter_id'] }}" data-bs-parent="#chapters">
                                <div class="accordion-body">
                                  {% if chapter['description'] != None %}
                                    <h6 class="h6 mb-2">Description:</h6>
                                    <p class="mb-2">{{ chapter['description'] }}</p>
                                  {% endif %}
                                      {% if chapter['lessons']|length > 0 %}
                                        <div class="accordion mb-3" id="lessons">
                                          {% for lesson in chapter['lessons'] %}
                                          <div class="accordion-item">
                                              <h2 class="accordion-header" id="heading{{ chapter['chapter_id'] }}_{{ lesson['lesson_id'] }}">
                                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{ chapter['chapter_id'] }}_{{ lesson['lesson_id'] }}" aria-expanded="false" aria-controls="collapse{{ chapter['chapter_id'] }}_{{ lesson['lesson_id'] }}">
                                                  Lesson {{ lesson['lesson_id'] }}: {{ lesson['title'] }}
                                                </button>
                                              </h2>
                                              <div id="collapse{{ chapter['chapter_id'] }}_{{ lesson['lesson_id'] }}" class="accordion-collapse collapse" aria-labelledby="panelsStayOpen-headingOne"  data-bs-parent="#lessons">
                                                <div class="accordion-body">
                                                  {{ lesson['content'] }}
                                                </div>
                                              </div>
                                            </div>
                                          {% endfor %}
                                        </div>
                                      {% else %}
                                      <div class="col-12">
                                        <h6 class="mb-3">There are not registered lessons yet </h1>
                                      </div>
                                      {% endif %}
                                      <button type="button" class="btn btn-outline-primary mb-3" data-bs-chapter="{{ chapter['chapter_id'] }}" data-bs-course="{{ course['id'] }}" data-bs-toggle="modal" data-bs-target="#addLessonModal">Add Lesson</button>
                                    </div>
                                </div>
                            </div>
                           {% endfor %}
                        </div>
                      {% else %}
                          <div class="col-xs-12">
                            <h6 class="mb-3">There are not registered chapters yet </h1>
                          </div>
                      {% endif %}
                  <button type="button" class="btn btn-outline-primary mb-3" data-bs-toggle="modal" data-bs-target="#addChapterModal">Add Chapter</button>
              </div>
          </div>
  ```

