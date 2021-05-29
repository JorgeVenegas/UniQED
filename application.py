import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

MESSAGES = []

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")

@app.route("/", methods=["GET", "POST"])
def index():
    missing = False
    if request.method == "POST":

        # TODO: Add the user's entry into the database

        name = request.form.get("name")
        if not name:
            MESSAGES.append("Missing name.")
            missing = True

        month = request.form.get("month")
        if not month:
            MESSAGES.append("Missing month.")
            missing = True

        day = request.form.get("day")
        if not day:
            MESSAGES.append("Missing day.")
            missing = True

        if missing:
            #return
            return render_template("missing.html", messages=MESSAGES)

        db.execute("INSERT INTO birthdays (name, month, day) VALUES(?, ?, ?)", name, month, day)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays ")

        return render_template("index.html", birthdays=birthdays)

@app.route("/remove", methods=["GET", "POST"])
def remove():
    missing = False
    if request.method == "POST":

        # TODO: Add the user's entry into the database

        name = request.form.get("name")
        if not name:
            MESSAGES.append("Missing name.")
            missing = True

        if missing:
            #return
            return render_template("missing.html", messages=MESSAGES)

        db.execute("DELETE FROM birthdays WHERE name = ?", name)

        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays ")

        return render_template("remove.html", birthdays=birthdays)

@app.route("/edit", methods=["GET", "POST"])
def edit():
    missing = False
    if request.method == "POST":

        # TODO: Add the user's entry into the database

        name = request.form.get("name")
        if not name:
            MESSAGES.append("Missing name.")
            missing = True

        a_month = request.form.get("a_month")
        if not a_month:
            MESSAGES.append("Missing actual month.")
            missing = True

        a_day = request.form.get("a_day")
        if not a_day:
            MESSAGES.append("Missing actual day.")
            missing = True

        n_month = request.form.get("n_month")
        if not n_month:
            MESSAGES.append("Missing new month.")
            missing = True

        n_day = request.form.get("n_day")
        if not n_day:
            MESSAGES.append("Missing new day.")
            missing = True


        if missing:
            #return
            return render_template("missing.html", messages=MESSAGES)

        db.execute("UPDATE birthdays SET month = ?, day = ? WHERE name = ? AND month = ? AND day = ?", n_month, n_day, name, a_month, a_day)


        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html
        birthdays = db.execute("SELECT * FROM birthdays ")

        return render_template("edit.html", birthdays=birthdays)
