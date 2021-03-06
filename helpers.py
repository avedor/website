import re
<<<<<<< HEAD
import os
=======
>>>>>>> aa9df2df2f58b5f3dae5518eee9736fb214c4185

import requests
from functools import wraps
from flask import render_template, session

def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))

def has_caps(inputString):
    return bool(re.search(r'[A-Z]', inputString))

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

#########################################################
### Change api key after grading - and switch to .env ###
#########################################################
# Declare mail
mailgun_api_key="b6f1ad22f463ca74532d5b7c3845edc0-fb87af35-243cba96"
<<<<<<< HEAD
mailgun_api_key= os.environ.get("MAILGUN_API_KEY")
=======
>>>>>>> aa9df2df2f58b5f3dae5518eee9736fb214c4185
mailgun_url="https://api.mailgun.net/v3/mail.averydorgan.com/messages"

# Enable sending of emails
def send_mail(sender_name, sender_email, message):
    requests.post(mailgun_url,
        auth=("api", mailgun_api_key),
        data={
             "from": "{}".format(sender_email),
             "to": "avery@averydorgan.com",
             "subject": "Contact Form Submission",
             "text": "{}:\n\n{}".format(sender_name, message)
            }
        )
