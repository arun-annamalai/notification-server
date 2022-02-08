import os

from notification_server import Server


def print_hello():
    notify = True
    subject = "Contents"
    msg = "This message is sent from Python"
    return notify, msg, subject


notifier = Server()
notifier.register_emailer(os.environ['EMAIL'], os.environ['EMAIL_PASSWORD'])
notifier.register_number(os.environ['NUMBER'], "sprint")

notifier.minutely_job(func=print_hello)
notifier.start()
