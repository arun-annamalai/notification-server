import os
import smtplib
import time
from email.message import EmailMessage


class Listserv:
    def __init__(self):
        self.emails = []
        self.numbers = []

    def register_number(self, number: str, carrier: str):
        self.numbers.append(Number(number, carrier))

    def register_email(self, email_address: str):
        self.emails.append(email_address)

    def get_emails(self):
        return self.emails

    def get_numbers(self):
        return self.numbers


class CustomEmail:
    def __init__(self, email_address: str):
        self.email = email_address


class Number:
    def __init__(self, phone_number: str, carrier: str):
        self.phone_number = phone_number
        self.carrier = carrier


class Emailer:
    def __init__(self, sender_email: str, sender_pass: str):
        self.send_interval = 5
        self.carrier_dict = {"verizon": "vtext.com",
                             "tmobile": "tmomail.net",
                             "sprint": "messaging.sprintpcs.com",
                             "att": "txt.att.net"}

        self.sender_email = sender_email
        self.sender_pass = sender_pass

    def send_message(self, listserv: Listserv, content: str, subject: str = None):
        self._send_text_mail(listserv.get_numbers(), content, subject)
        self._send_regular_mail(listserv.get_emails(), content, subject)

    def _send_regular_mail(self, emails: list, content, subject=None):
        if emails is None or len(emails) == 0:
            return
        
        msg = EmailMessage()

        if subject:
            msg['Subject'] = subject

        msg['From'] = self.sender_email
        if len(emails) == 1:
            msg['To'] = emails
        else:
            msg['To'] = ', '.join(emails)

        msg.set_content(content)

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_pass)
            server.send_message(msg)

    def _send_text_mail(self, listserv: list, content, subject=None):
        for number in listserv:
            sms_gateway = number.phone_number + "@" + self.carrier_dict[number.carrier]
            self._send_regular_mail([sms_gateway], content, subject)
            time.sleep(self.send_interval)


if __name__ == '__main__':
    e = Emailer(os.environ['EMAIL'], os.environ['EMAIL_PASSWORD'])
    listserv = Listserv()
    listserv.register_email(os.environ['PERSONAL_EMAIL'])
    listserv.register_number(os.environ['NUMBER'], "sprint")

    e.send_message(listserv, "hello", None)
