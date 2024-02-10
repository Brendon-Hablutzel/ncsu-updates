import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from get_vars import get_gmail_username, get_gmail_app_password


class NotificationSystem:
    def __init__(self):
        self.smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.gmail_username = get_gmail_username()
        gmail_app_password = get_gmail_app_password()
        self.smtp_server.login(self.gmail_username, gmail_app_password)

        self.initialized_server = True

    def close(self):
        self.smtp_server.quit()

    # for email, recipients is an email address
    def send_notification(self, recipient: str, title: str, message: str):
        if not self.initialized_server:
            raise Exception(
                "must initialize server using a context manager before sending notifications")

        msg = MIMEMultipart()
        msg["Subject"] = title
        msg["From"] = f"{self.gmail_username}@gmail.com"
        msg["To"] = recipient

        msg.attach(MIMEText(message, "plain"))

        self.smtp_server.sendmail(f"{self.gmail_username}@gmail.com",
                                  recipient, msg.as_string())
