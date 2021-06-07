from requests import post
import requests
from django.conf import settings

def send_contact_mail(sender, message):
    return requests.post(
        settings.MAILGUN_API_URL,
        auth = ("api", settings.MAILGUN_API_KEY),
        data = {
            "from": f"Użytkownik Herculesa {sender}",
            "to": "kr4wczyk13@gmail.com",
            "subject": "Nowa wiadomość w systemie Hercules!",
            "text": message,
        }
    )