from requests import post
import requests
import os

def send_contact_mail(sender, message):
    url = os.environ.get("MAILGUN_API_URL")
    key = os.environ.get("MAILGUN_API_KEY")
    return requests.post(
        url,
        auth = ("api", key),
        data = {
            "from": f"Użytkownik Herculesa {sender}",
            "to": "kr4wczyk13@gmail.com",
            "subject": "Nowa wiadomość w systemie Hercules!",
            "text": message,
        }
    )