import random
from django.contrib.auth.mixins import UserPassesTestMixin


def send_otp(request, email):
    otp_code = str(random.randint(100000, 999999))
    request.session['otp_code'] = otp_code
    print(f"OTP for {email}: {otp_code}")


def verify_otp(saved_code, submitted_code):
    return saved_code == submitted_code


