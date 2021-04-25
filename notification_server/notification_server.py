import threading
import time
import smtplib, ssl
import os
import schedule

class notification_server:
    def __init__(self, threading = False):
        self.threading = threading
        self.refresh_interval = None
        self.internal_scheduler = schedule.Scheduler()
        self.emails = []
        self.numbers = []


    def __send_notification(self, msg):
        pass

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


    def __add_job(self, func):
        wrapped_func = self.__notification_wrapper(func)
        if self.threading:
            wrapped_func = self.__transform_to_threaded_job(wrapped_func)
        else:
            pass

    def weekly_job(self, func):
        pass

    def hourly_job(self, func):
        pass

    def daily_job(self, func):
        pass

    def register_email(self, email, password):
        self.emails.append((email, password))

    def register_number(self, number, carrier):
        self.numbers.append((number, carrier))

    def start(self):
        if self.refresh_interval is None:
            raise Exception("atleast one job must be specified")

        while True:
            self.internal_scheduler.run_pending()
            time.sleep(self.refresh_interval)



if __name__ == '__main__':
    port = 465  # For SSL
    sender_email = os.environ['EMAIL1']
    password = os.environ['EMAIL_PASS']

    receiver_email = os.environ['EMAIL2']
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)