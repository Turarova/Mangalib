from .celery import  app
# import random
# import string
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# from .helpers import  send_confirmation_email

# @app.task
# def send_conf_emails(email, code):
#     send_confirmation_email(email, code)

@app.task
def send_pass_res(email):
    context = {
        "email_text_detail": "That's your new password",
        "email": email
        # "new_password": ''.join(random.choice(string.ascii_lowercase + string.digits, k = 8))
    }

    msg_html = render_to_string("email.html", context)
    subject = "Password reset"
    plain_message = strip_tags(msg_html)
    recipient_list = email
    mail.send_mail(
        subject,
        plain_message,
        "maviboncuaika@gmail.com",
        recipient_list,
        html_message= msg_html
    )

