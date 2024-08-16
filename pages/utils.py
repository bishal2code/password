from django.core.mail import send_mail
from django.conf import settings

def send_email_to_client(name,sendTo,code):
    subject = "Verification Code"
    message = f"Dear {name}<br> Code : {code}"
    from_email = settings.EMAIL_HOST_USER
    reciptient_list = [f"{sendTo}"]
    send_mail(subject,message,from_email,reciptient_list)