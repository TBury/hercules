from requests import post
import requests
import os


def send_contact_mail(sender, message):
    return requests.post(
        os.environ.get("MAILGUN_API_URL"),
        auth = ("api", os.environ.get("MAILGUN_API_KEY")),
        data = {
            "from": f"Użytkownik Herculesa {sender}",
            "to": "kr4wczyk13@gmail.com",
            "subject": "Nowa wiadomość w systemie Hercules!",
            "text": message,
        }
    )