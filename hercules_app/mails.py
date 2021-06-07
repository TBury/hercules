from requests import post
import requests
import os

from dotenv import load_dotenv
load_dotenv()

def send_contact_mail(sender, message):
    url = os.getenv("MAILGUN_API_URL")
    key = os.getenv("MAILGUN_API_KEY")
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