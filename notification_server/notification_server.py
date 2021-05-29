import threading
import time
import smtplib, ssl
import os
import schedule

carrier_dict = {"verizon": "vtext.com",
                "tmobile": "tmomail.net",
                "sprint": "messaging.sprintpcs.com",
                "att": "txt.att.net"}

class server:
    def __init__(self, threading = False):
        self.threading = threading
        self.refresh_interval = None
        self.internal_scheduler = schedule.Scheduler()
        self.emails = []
        self.numbers = []
        self.text_on = False


    def __send_notification(self, msg):
        print("HELLO")
        context = ssl.create_default_context()
        port = 465  # For SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.emails[0][0], self.emails[0][1])
            for receiver_email in self.emails:
                server.sendmail(self.emails[0][0], receiver_email, msg)
                time.sleep(2)

            if self.text_on:
                for number in self.numbers:
                    print("sending text")
                    receiver_sms_gateway = str(number[0]) + "@" + carrier_dict[number[1]]
                    server.sendmail(self.emails[0][0], receiver_sms_gateway, msg)

    def __update_refresh_interval(self, new_interval):
        if not self.refresh_interval:
            self.refresh_interval = new_interval * 60
        else:
            self.refresh_interval = min(self.refresh_interval, new_interval * 60)

    def __transform_to_threaded_job(self, func):
        def threaded_job():
            t = threading.Thread(func)
            t.start()
        return threaded_job

    def __notification_wrapper(self, func):
        def notification_job():
            notify, msg = func()
            if notify:
                self.__send_notification(msg)

        return notification_job

    def __add_job(self, func, m):
        notif_wrapped_func = self.__notification_wrapper(func)
        if self.threading:
            notif_wrapped_func = self.__transform_to_threaded_job(notif_wrapped_func)

        self.internal_scheduler.every(m).minutes.do(notif_wrapped_func)

    def weekly_job(self, func):
        self.__update_refresh_interval(60*24*7)
        self.__add_job(func, 60 * 24 * 7)

    def daily_job(self, func):
        self.__update_refresh_interval(60*24)
        self.__add_job(func, 60 * 24)

    def hourly_job(self, func):
        self.__update_refresh_interval(60)
        self.__add_job(func, 60)

    def minutely_job(self, func):
        self.__update_refresh_interval(1)
        self.__add_job(func, 1)

    def register_email(self, email, password):
        self.emails.append((email, password))

    def register_number(self, number, carrier):
        self.text_on = True
        self.numbers.append((number, carrier))

    def start(self):
        if self.refresh_interval is None:
            raise Exception("atleast one job must be specified")

        if not len(self.emails):
            raise Exception("register email before starting")

        while True:
            self.internal_scheduler.run_pending()
            time.sleep(self.refresh_interval)


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

    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    message = MIMEMultipart()
    message['From'] = "aannamal@umich.edu"
    message['To'] = "2488805628" + "@" + carrier_dict["sprint"]
    message['Subject'] = "Sent from Arun!"

    text = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
            % (message['From'], ", ".join(message['To']), message['Subject']))
    text += "Hello World!\r\n"

    text = "\r\nHello World!"
    message.attach(MIMEText(text.encode("utf-8"), "plain", "utf-8"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(message["From"], "Liculdedav8")

    # server.sendmail(message["From"], [message["To"]], text)
    server.send_message(message)
