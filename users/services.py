import random
from twilio.rest import Client
import os


def generate_code():
    code = random.randint(1000, 9999)
    return code


def send_otp(code, phone):
    twilio_sid = os.getenv('TWILIO_SID')
    twilio_token = os.getenv('TWILIO_TOKEN')
    twilio_phone = os.getenv('TWILIO_PHONE')

    client = Client(twilio_sid, twilio_token)

    message = client.messages.create(
        from_=twilio_phone,
        body=f'Ваш код подтверждения - {code}',
        to='+7'+phone,
    )

    print(message.sid)
    print(message.status)
