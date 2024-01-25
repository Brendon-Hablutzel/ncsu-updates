import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List


def get_secret(secret_name: str):
    secret = os.getenv(f"{secret_name}")

    if secret is None:
        raise Exception(f"secret {secret_name} not found")

    return secret


class NotificationSystem:
    def __init__(self):
        self.smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.gmail_username = get_secret("GMAIL_USERNAME")
        gmail_app_password = get_secret("GMAIL_APP_PASSWORD")
        self.smtp_server.login(self.gmail_username, gmail_app_password)

    def __del__(self):
        self.smtp_server.quit()

    # for email, recipients is a list of email addresses
    def send_notification(self, recipients: List[str], title: str, message: str):
        msg = MIMEMultipart()
        msg["Subject"] = title
        msg["From"] = f"{self.gmail_username}@gmail.com"
        msg["To"] = ", ".join(recipients)

        msg.attach(MIMEText(message, "plain"))

        self.smtp_server.sendmail(f"{self.gmail_username}@gmail.com",
                                  recipients, msg.as_string())
