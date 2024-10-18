from typing import List
from celery import Celery
from asgiref.sync import async_to_sync

from src.mail import mail, create_message


c_app = Celery()

c_app.config_from_object("src.config")


@c_app.task()
def send_email(recipients: List[str], subject: str, body: str):
    message = create_message(recipients=recipients, subject=subject, body=body)

    async_to_sync(mail.send_message)(message)
    print("Email Sent")
