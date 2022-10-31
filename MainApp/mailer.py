from django.core.mail import send_mail

def send_email(subject, message, address_from, addresses_to):
    send_mail(
        subject,
        message,
        address_from,
        addresses_to,
        fail_silently=False,
    )