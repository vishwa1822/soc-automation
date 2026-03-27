import time
import random
from logger import send_log


def generate_background_logs():

    endpoints = [
        "/login",
        "/profile",
        "/dashboard"
    ]

    while True:

        resource = random.choice(endpoints)

        send_log(
            event_type="normal_activity",
            resource=resource,
            ip="127.0.0.1"
        )

        time.sleep(10)