from django.core.mail import send_mail

def send_contact_mail(sender, message):
    subject = "Nowa wiadomość w systemie Hercules!"
    recipient_list = ['kr4wczyk13@gmail.com']
    send_mail(
        subject,
        message,
        sender,
        recipient_list
    )