import os
import threading
import time

import schedule

from notification_server.email_utility import Listserv, Emailer


class Server:
    def __init__(self, threaded=False):
        self.threaded = threaded
        self.refresh_interval = None
        self.internal_scheduler = schedule.Scheduler()
        self.list_serve = Listserv()
        self.emailer = None

    def __send_notification(self, msg, subject=None):
        print("SENDING NOTIFICATION")
        self.emailer.send_message(self.list_serve, msg, subject)

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
            notify, msg, subject = func()
            if notify:
                self.__send_notification(msg, subject)

        return notification_job

    def __add_job(self, func, m):
        notif_wrapped_func = self.__notification_wrapper(func)
        if self.threaded:
            notif_wrapped_func = self.__transform_to_threaded_job(notif_wrapped_func)

        self.internal_scheduler.every(m).minutes.do(notif_wrapped_func)

    def weekly_job(self, func):
        self.__update_refresh_interval(60 * 24 * 7)
        self.__add_job(func, 60 * 24 * 7)

    def daily_job(self, func):
        self.__update_refresh_interval(60 * 24)
        self.__add_job(func, 60 * 24)

    def hourly_job(self, func):
        self.__update_refresh_interval(60)
        self.__add_job(func, 60)

    def minutely_job(self, func):
        self.__update_refresh_interval(1)
        self.__add_job(func, 1)

    def register_email(self, email):
        self.list_serve.register_email(email)

    def register_number(self, number, carrier):
        self.list_serve.register_number(number, carrier)

    def register_emailer(self, email, password):
        self.emailer = Emailer(email, password)

    def start(self):
        if self.refresh_interval is None:
            raise Exception("atleast one job must be specified")

        if not self.emailer:
            raise Exception("register emailer before starting")

        while True:
            self.internal_scheduler.run_pending()
            time.sleep(self.refresh_interval)


if __name__ == '__main__':
    ns = Server()

    ns.register_emailer(os.environ['EMAIL'], os.environ['EMAIL_PASSWORD'])

    ns.register_number(os.environ['NUMBER'], "sprint")
