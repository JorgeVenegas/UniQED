# export API_KEY=pk_bf75a454b4774756b7730b6028af728b

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    shares = db.execute("SELECT purchases.symbol, SUM(purchases.quantity), SUM(purchases.price) FROM users INNER JOIN purchases ON users.id = purchases.user_id GROUP BY purchases.symbol")

    total = 0

    for share in shares:
        values = lookup(share["symbol"])
        share["name"] = values["name"]
        share["price"] = values["price"]
        total += share["SUM(purchases.price)"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    total += cash[0]["cash"]

    return render_template("index.html", shares=shares, cash=cash, total=total)
    # return apology("TODO", 403)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure fill of a correct symbol
        symbol = request.form.get("symbol")

        # Lookup for corresponding values
        lvalues = lookup(symbol)

        if not symbol or lvalues == None:
            return apology("Invalid symbol. Try again", 403)

        # Ensure fill of a correct shares
        shares = float(request.form.get("shares"))

        if not shares or not shares.is_integer() or not shares > 0:
            return apology("Invalid number of shares. Try again", 403)

        # Necessary info for transaction
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]
        cost = float(lvalues["price"]) * shares

        # Check if enough cash to buy
        if cost > cash:
            return apology("Unable to complete purchase. Not enough cash to proceed. Try again", 403)

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - cost, session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, quantity, price, i_price) VALUES (?, ?, ?, ?, ?)", session["user_id"], symbol, shares, cost, lvalues["price"])

        # Show corresponding values for stock symbol
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    purchases = db.execute("SELECT * FROM purchases WHERE user_id = ?", session["user_id"])

    return render_template("history.html", purchases=purchases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure fill of a correct symbol
        symbol = request.form.get("symbol")

        if not symbol or lookup(symbol) == None:
            return apology("Invalid symbol. Try again", 403)

        # Lookup for corresponding values
        values=lookup(symbol)

        # Show corresponding values for stock symbol
        return render_template("quoted.html", values=values)

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure fill of a correct username
        username = request.form.get("username")
        usernames = db.execute("SELECT * from users WHERE username = ?", username)

        if not username or len(usernames) != 0:
            return apology("Invalid usernamte. Try again", 400)

        # Ensure fill of a correct password
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not password or not confirmation or password != confirmation:
            return apology("Passwords do not match. Try again", 400)

        # Insert registrant info in database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, generate_password_hash(password))

        # Redirect to login
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure fill of a correct username
        share = request.form.get("shares")
        shares = db.execute("SELECT purchases.symbol FROM users INNER JOIN purchases ON users.id = purchases.user_id GROUP BY purchases.symbol")

        symbols = []

        for shr in shares:
            symbols.append(shr["symbol"])

        print(symbols)
        if share not in symbols:
            return apology("Invalid share. Try again", 403)

        number = float(request.form.get("number"))
        owned = db.execute("SELECT SUM(purchases.quantity) AS quantity FROM users INNER JOIN purchases ON users.id = purchases.user_id WHERE purchases.symbol = ?", share)

        if number > owned[0]["quantity"]:
            return apology("Too much shares. Try again", 403)

        if not number:
            return apology("Missing value. Try again", 403)

        if not number.is_integer() or not number > 0:
            return apology("Invalid value. Try again", 403)

        actual = lookup(share)
        income = float(actual["price"]) * number

        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]

        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + income, session["user_id"])
        db.execute("INSERT INTO purchases (user_id, symbol, quantity, price, i_price) VALUES (?, ?, ?, ?, ?)", session["user_id"], share, -number, -income, actual["price"])

        # Redirect to login
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        shares = db.execute("SELECT purchases.symbol FROM users INNER JOIN purchases ON users.id = purchases.user_id GROUP BY purchases.symbol")
        return render_template("sell.html", shares=shares)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
