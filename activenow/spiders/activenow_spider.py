import json
import os
from functools import cached_property
import smtplib
import scrapy
from scrapy import FormRequest
from scrapy.http import Request
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class ActiveNowSpider(scrapy.Spider):
    name = "active_now"
    json_pth = "db.json"  # to store available dates
    login_url = "https://app.activenow.io/users/sign_in"
    next_url = "https://app.activenow.io/client_panel/cancellations/making_up_absences"

    def start_requests(self):
        urls = [self.login_url]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        return [
            FormRequest.from_response(
                response,
                formdata={
                    "user[email]": os.getenv("ACTIVE_NOW_USERNAME", ""),
                    "user[password]": os.getenv("ACTIVE_NOW_PASSWORD", ""),
                },
                callback=self.after_login_go_to_next_url,
            )
        ]

    def after_login_go_to_next_url(self, response):
        if "Błędny adres email lub hasło" in response.text:
            raise Exception("Invalid ActiveNow credentials.")
        return Request(url=self.next_url, callback=self.parse_cancellations_page)

    @cached_property
    def prev_data(self):
        if not os.path.exists(self.json_pth):
            return []
        with open(self.json_pth, "r") as fp:
            return json.loads(fp.read())

    def update_data(self, data):
        with open(self.json_pth, "w+") as fp:
            fp.write(json.dumps(data))

    def send_notification(self, data):
        sender_address = os.getenv("DEFAULT_FROM_EMAIL", "")
        sender_pass = os.getenv("EMAIL_PASSWORD", "")
        receiver_address = os.getenv("RECEIVER_EMAIL", "")

        message = MIMEMultipart()
        message["From"] = sender_address
        message["To"] = receiver_address
        message[
            "Subject"
        ] = "ActiveNow:odrabianie -> dostępne terminy"  # The subject line
        # The body and the attachments for the mail
        mail_content = "\n".join([str(row) for row in data])
        message.attach(MIMEText(mail_content, "plain"))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP(
            os.getenv("EMAIL_SMTP", ""), os.getenv("EMAIL_PORT", 587)
        )  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()

    def parse_cancellations_page(self, response):
        current_data = []
        for row in response.css("#content .card")[0].css("tbody tr"):
            cols = row.css("td::text")
            current_data.append(
                {
                    "group": cols[0].get(),
                    "date": cols[1].get(),
                    "place": cols[2].get(),
                    "coach": cols[3].get(),
                    "level": cols[4].get(),
                    "capacity": cols[5].get(),
                }
            )
        if self.prev_data != current_data:
            self.send_notification(current_data)
            self.update_data(current_data)
