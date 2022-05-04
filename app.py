import os

from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from helpers import send_mail, login_required, apology


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///users.db")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Load main website for general public
@app.route("/")
def index():
    return render_template("index.html")

# Load about page
@app.route("/about")
def about():
    return render_template("about.html")


### May need to revisit the contact page
# Load contact page
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        # ensure all the required parts of the form are filled out
        if not request.form.get("name"):
            return None
        elif not request.form.get("email"):
            return None
        elif not request.form.get("message"):
            return None
        sender = request.form.get("email")
        message = request.form.get("message")
        send_mail(sender, message)
        return redirect("/")
    else:
        return render_template("contact.html")

# Load project page
@app.route("/projects")
def projects():
    return render_template("projects.html")

# Allow user to log in
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
        return redirect("/logged_in")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logged_in")
@login_required
def handle_login():
    # consider adding a pretty url before submitting
    return redirect("http://192.168.1.20:8087", code=302)


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to home page
    return redirect("/")
