import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import time

carrier_dict = {"verizon": "vtext.com",
                "tmobile": "tmomail.net",
                "sprint": "messaging.sprintpcs.com",
                "att": "txt.att.net"}
class emailer:
    def __init__(self, sender_email, sender_pass):
        self.send_interval = 5
        self.carrier_dict = {"verizon": "vtext.com",
                            "tmobile": "tmomail.net",
                            "sprint": "messaging.sprintpcs.com",
                            "att": "txt.att.net"}

        self.sender_email = sender_email
        self.sender_pass = sender_pass

    def send_regular_mail(self, listserv, content=None):
        msg = EmailMessage()


        msg['Subject'] = f'The contents'
        msg['From'] = self.sender_email
        if len(listserv) == 1:
            msg['To'] = listserv
        else:
            msg['To'] = ', '.join(listserv)
        if content:
            msg.set_content(content)
        else:
            msg.set_content("hello")

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_pass)
            server.send_message(msg)

    def send_text_mail(self, listserv, content=None):
        for num, carrier in listserv:
            sms_gateway = num + "@" + self.carrier_dict[carrier]
            self.send_regular_mail([sms_gateway], content)
            time.sleep(self.send_interval)

if __name__ == '__main__':
    # port = 465  # For SSL
    # sender_email = os.environ['EMAIL1']
    # password = os.environ['EMAIL_PASS']
    #
    # receiver_email = os.environ['EMAIL2']
    # message = """\
    # Subject: Hi there
    #
    # This message is sent from Python."""
    #
    # # Create a secure SSL context
    # context = ssl.create_default_context()
    #
    # receiver_sms_gateway = "2488805628" + "@" + "pm.sprint.com"
    #
    # with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    #     server.login(sender_email, password)
    #     server.sendmail(sender_email, receiver_sms_gateway, message)

    # message = MIMEMultipart()
    # message['From'] = "aannamal@umich.edu"
    # message['To'] = "2488805628" + "@" + carrier_dict["sprint"]
    # message['Subject'] = "Sent from Arun!"
    #
    # text = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
    #         % (message['From'], ", ".join(message['To']), message['Subject']))
    # text += "Hello World!\r\n"
    #
    # text = "\r\nHello World!"
    # message.attach(MIMEText(text.encode("utf-8"), "plain", "utf-8"))
    #
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(message["From"], "Liculdedav8")
    #
    # # server.sendmail(message["From"], [message["To"]], text)
    # server.send_message(message)


    e = emailer("aannamal@umich.edu", "Liculdedav8")
    listserv = [("2488805628", "sprint")]
    e.send_text_mail(listserv)
