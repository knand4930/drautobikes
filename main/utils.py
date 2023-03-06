import random

import requests


def send_otp_to_phone(phone_number):
    try:
        otp = random.randint(99999, 999999)
        # url = "messages url"
        # response = requests.get(url)
        # print(response)
        return otp
    except Exception as e:
        print(e)
        return None
