from django.conf import settings

from requests import post
import requests

def send_contact_mail(sender, message):
    url = f"https://api.eu.mailgun.net/v3/{settings.MAILGUN_API_URL}" 
    key = settings.MAILGUN_API_KEY
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