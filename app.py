import os
import re

from cs50 import SQL
from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import send_mail, login_required, apology, has_numbers, has_caps


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

###########################################################################
### After submission, change to a production ready db - likely postgres ###
###########################################################################
# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database/users.db")
# Create the users table if it doesn't already exist
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT NOT NULL, hash TEXT NOT NULL)")

# Handle all the headers!
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

############################################
### May need to revisit the contact page ###
############################################
# Load contact page
@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        # Do some basic form validation
        if not request.form.get("name"):
            return apology("must provide name", 400)
        elif not request.form.get("email"):
            return apology("must provide email", 400)
        elif not re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",request.form.get("email")):
            return apology("invalid email", 400)
        elif not request.form.get("message"):
            return apology("must provide message", 400)
        sender_name = request.form.get("name")
        sender_email = request.form.get("email")
        message = request.form.get("message")
        # Use helper to send myself an email with the contact form fields
        send_mail(sender_name, sender_email, message)
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
    # will change to something internal after grading
    return redirect("http://cs50.averydorgan.local", code=302)


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to home page
    return redirect("/")

################################
### Remove after registering ###
################################
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure password is 8+ chars
        elif len(request.form.get("password")) < 8:
            return apology("password too short", 400)
        # Ensure password contains 1+ number
        elif has_numbers(request.form.get("password")) == False:
            return apology("password needs number", 400)
        # Ensure password contains 1+ cap
        elif has_caps(request.form.get("password")) == False:
            return apology("password needs cap", 400)
        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        # Ensure passwords match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 0:
            return apology("already registered", 400)
        # Hash password
        hash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)
        # Register user if pass all sanity checks
        rows = db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"), hash)
        # Redirect user to home page
        return redirect("/login")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")
