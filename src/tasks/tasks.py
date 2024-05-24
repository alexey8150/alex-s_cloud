import smtplib
from jinja2 import Template
from email.message import EmailMessage
from celery import Celery

from settings import SMTP_PASSWORD, SMTP_USER, SMTP_HOST, SMTP_PORT
from notifications import confirm_code_template, password_mail_template
celery = Celery('tasks', broker='redis://localhost:6379')


@celery.task
def send_confirmation_email(email_user: str, confirm_code: str) -> None:
    email = EmailMessage()
    email['Subject'] = 'Подтверждение пользователя.'
    email['From'] = SMTP_USER
    email['To'] = email_user

    email_template = Template(confirm_code_template)

    email.set_content(email_template.render({'confirm_code': confirm_code}), subtype='html')
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)

@celery.task
def send_user_password(email_user: str, password: str) -> None:
    email = EmailMessage()
    email['Subject'] = 'Пароль нового пользователя.'
    email['From'] = SMTP_USER
    email['To'] = email_user

    email_template = Template(password_mail_template)

    email.set_content(email_template.render({'password': password}), subtype='html')
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)