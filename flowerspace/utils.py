import random
from django.contrib.auth.mixins import UserPassesTestMixin
from onlineshop.models import Order
from django.core.mail import send_mail


RECEIVER_EMAIL = 'projectspacedevs@gmail.com'

def send_otp(request, email):
    otp_code = str(random.randint(100000, 999999))
    request.session['otp_code'] = otp_code
    send_mail("Your otp code", f"Flowerspace OTP code for your email: {otp_code}", RECEIVER_EMAIL, [email,])


def verify_otp(saved_code, submitted_code):
    return saved_code == submitted_code



def send_contact_mail(name, email, desc):
    message = f"""
❊❋✽✾✿❀❁❃⚘⚜✤☘ꕥꕤ
from: {name} 
                
email: {email}
                
message: 
{desc}
❊❋✽✾✿❀❁❃⚘⚜✤☘ꕥꕤ
"""
    send_mail(name, message, email, [RECEIVER_EMAIL,])




