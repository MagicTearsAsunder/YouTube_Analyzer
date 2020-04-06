from django.core.mail import send_mail
from django.conf import settings


def send_email_confirmation(new_user, host_url):
    the_link = f'http://{host_url}/confirm/{new_user.random_url}'
    e_mail = new_user.email
    mail_body = (
        f"{new_user.username}, welcome to Omae Wa Mou Shindeiru!\n\n"
        "Thanks for creating an Omae Wa account.\n"
        "Click the link below to confirm your email address.\n\n"
        f"{the_link}"
    )

    send_mail(
        'Registration',
        mail_body,
        settings.EMAIL_HOST_USER,
        [f'{e_mail}']
    )
