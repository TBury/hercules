from django.conf import settings

from requests import post
import requests
import os


def send_contact_mail(sender, message):
    url = settings.MAILGUN_API_URL
    key = settings.MAILGUN_API_KEY
    print(url)
    print(key)
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