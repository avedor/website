import requests

# Declare mail
mailgun_api_key="b6f1ad22f463ca74532d5b7c3845edc0-fb87af35-243cba96"
mailgun_url="https://api.mailgun.net/v3/mail.averydorgan.com/messages"

def send_mail(sender, message):
    requests.post(mailgun_url,
        auth=("api", mailgun_api_key),
        data={
             "from": sender,
             "to": "avery@averydorgan.com",
             "subject": "Contact Form Submission",
             "text": message
            }
        )