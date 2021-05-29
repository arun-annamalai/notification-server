import os
from notification_server import server


def print_hello():
    msg = "This message is sent from Python"
    return True, msg

notifier = server()
notifier.register_email(os.environ['EMAIL1'], os.environ['EMAIL_PASS'])
notifier.register_number("2488805628", "sprint")

notifier.minutely_job(func=print_hello)
notifier.start()
