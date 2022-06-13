import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .base import BaseNotificationBackend


class EmailBackend(BaseNotificationBackend):
    default_from_email = os.getenv("DEFAULT_FROM_EMAIL", "")
    email_password = os.getenv("EMAIL_PASSWORD", "")
    receiver_email = os.getenv("RECEIVER_EMAIL", default_from_email)

    def run(self):
        message = MIMEMultipart()
        message["From"] = self.default_from_email
        message["To"] = self.receiver_email
        message["Subject"] = self.subject  # The subject line
        # The body and the attachments for the mail
        # mail_content = "\n".join([str(row) for row in data])
        message.attach(MIMEText(self.message, "plain"))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP(
            os.getenv("EMAIL_SMTP", ""), os.getenv("EMAIL_PORT", 587)
        )  # use gmail with port
        session.starttls()  # enable security
        session.login(
            self.default_from_email, self.email_password
        )  # login with mail_id and password
        text = message.as_string()
        session.sendmail(self.default_from_email, self.receiver_email, text)
        session.quit()
